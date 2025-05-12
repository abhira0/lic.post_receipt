from urllib.parse import quote_plus, unquote_plus
import os
import pythoncom
import traceback
from flask import Flask, redirect, render_template, request, jsonify

from foundation import InitialWipeOut, Printer, ScannedImage, logger

app = Flask(__name__)

FLASK_IP = "127.0.0.1"
FLASK_PORT = "1234"

# We'll only keep one scan at a time
CURRENT_SCAN = None
SCAN_ERROR = ""

# Create required directories if they don't exist
def ensure_directories():
    try:
        if not os.path.exists("static"):
            os.makedirs("static", exist_ok=True)
        if not os.path.exists("static/tmp"):
            os.makedirs("static/tmp", exist_ok=True)
    except Exception as e:
        logger.error(f"Error creating directories: {str(e)}")


@app.route("/")
def home():
    """Render the home page with the current scan if available."""
    global CURRENT_SCAN
    if CURRENT_SCAN:
        images = {CURRENT_SCAN["scanned_image_path"]: CURRENT_SCAN}
    else:
        images = {}
    return render_template("home.html", images=images, SCAN_ERROR=SCAN_ERROR)


@app.route("/clear")
def clear():
    """Clear the current scan data and return to home page."""
    global CURRENT_SCAN, SCAN_ERROR
    CURRENT_SCAN = None
    SCAN_ERROR = ""
    return redirect("/")


@app.route("/scan")
def scan():
    """Handle scanning process."""
    global SCAN_ERROR, CURRENT_SCAN
    
    # Reset any previous scan
    CURRENT_SCAN = None
    
    try:
        # Initialize COM for Windows
        pythoncom.CoInitialize()
        
        # Scan the object and return the absolute path of the scanned image
        printer = Printer()
        scanned_image_path = printer.acquire_image_wia()
        
        if not scanned_image_path:
            SCAN_ERROR = "Scanning failed. Please check your scanner connection."
            return redirect("/")
            
        scanned_image_path = f"http://{FLASK_IP}:{FLASK_PORT}/{scanned_image_path}"
        CURRENT_SCAN = {
            "scanned_image_path": scanned_image_path,
            "crop_url": f"/crop?scanned_image_path={quote_plus(scanned_image_path)}"
        }
        defaultCrop(scanned_image_path)
        SCAN_ERROR = ""
    except Exception as e:
        logger.error(f"Error during scanning: {str(e)}")
        logger.error(traceback.format_exc())
        SCAN_ERROR = (
            "1. Please turn on printer and connect it to your computer\n"
            "2. Do not turn off computer in the middle of the scan\n"
            f"3. Error details: {str(e)}"
        )
    return redirect("/")


@app.route("/crop")
def crop():
    """Render the crop interface for the scanned image."""
    try:
        scanned_image_path = unquote_plus(request.args["scanned_image_path"])
        return render_template("crop.html", scanned_image_path=scanned_image_path)
    except Exception as e:
        logger.error(f"Error in crop route: {str(e)}")
        global SCAN_ERROR
        SCAN_ERROR = f"Error preparing crop interface: {str(e)}"
        return redirect("/")


@app.route("/postCropInfo", methods=["POST"])
def postCropInfo():
    """Process the cropping information posted from the crop interface."""
    try:
        resp = request.json
        cropAndSave(resp)
        return jsonify({"status": "success", "message": "Image cropped successfully"})
    except Exception as e:
        logger.error(f"Error in postCropInfo: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500


def defaultCrop(scanned_image_path):
    """Apply default cropping to a newly scanned image."""
    try:
        resp = {
            "scanned_image_path": scanned_image_path,
            "x": 10,
            "y": 1855,
            "width": 685,
            "height": 295,
        }
        cropAndSave(resp)
    except Exception as e:
        logger.error(f"Error in defaultCrop: {str(e)}")
        logger.error(traceback.format_exc())
        raise


def cropAndSave(resp):
    """Crop the image according to given dimensions and save it as PNG and PDF."""
    global CURRENT_SCAN
    try:
        scanned_image_path = resp["scanned_image_path"]
        
        # Update the current scan data
        if CURRENT_SCAN and CURRENT_SCAN["scanned_image_path"] == scanned_image_path:
            CURRENT_SCAN.update(resp)
        else:
            CURRENT_SCAN = {
                "scanned_image_path": scanned_image_path,
                "crop_url": f"/crop?scanned_image_path={quote_plus(scanned_image_path)}"
            }
            CURRENT_SCAN.update(resp)
        
        # Process the image
        image = ScannedImage(scanned_image_path)
        cropped_image_path = image.crop(resp)
        CURRENT_SCAN["cropped_image_path"] = cropped_image_path
        pdf_path = image.saveAsPDF()
        CURRENT_SCAN["pdf_path"] = pdf_path
    except Exception as e:
        logger.error(f"Error in cropAndSave: {str(e)}")
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    try:
        ensure_directories()
        InitialWipeOut()
        app.run(host=FLASK_IP, port=FLASK_PORT, debug=True)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        logger.error(traceback.format_exc())