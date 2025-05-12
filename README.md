# Post LIC Receipt
## A WEB Tool

Python application that scans client addresses from a scanner and prints them on LIC post covers with precise dimensions.

__Written in: Python 3__

## Instruction Video on Youtube
**Coming soon**

## ___DISCLAIMER___
* *This project is done only for __educational purposes__*
* *If you are interested in creating any web scraper, you can learn through my projects*
* *I am __not responsible__ for any future __controversies/copyright issues__*
* *Making use of my project for any __illegal activities__ does not count as my responsibility*

# Table of Contents
- [Post LIC Receipt](#post-lic-receipt)
  - [A WEB Tool](#a-web-tool)
  - [Instruction Video on Youtube](#instruction-video-on-youtube)
  - [___DISCLAIMER___](#disclaimer)
- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Manual Setup](#manual-setup)
    - [Automated Setup](#automated-setup)
  - [Usage](#usage)
- [Technical Details](#technical-details)
  - [Features](#features)
  - [Source Code](#source-code)
  - [Contributing](#contributing)
  - [Version History](#version-history)
- [Thank You](#thank-you)

# Getting Started

## Prerequisites
* Operating System: Windows 10 (tested)
* Printer/Scanner: Canon 3100 (tested)
* Required software:
  * Python 3.10 or higher
  * Git (optional, for cloning the repository)

## Installation

### Manual Setup
1. Download and install git from [git-scm.com](https://git-scm.com/downloads "GIT-SCM")
2. Clone the repo on your Windows machine using:
   ```
   git clone https://github.com/abhira0/Post_LIC_Receipt
   ```
   Alternatively, download and extract the ZIP file from the repository.
3. Download Python 3.10 from [python.org](https://www.python.org/downloads/windows/ "Windows downloads")
4. Install Python, making sure to check "Add Python to PATH" during installation
5. Open a command prompt in the project directory and install dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Open the `postit.cmd` file in any text editor
7. Replace `<your_workspace>` with the actual path to the cloned repository

### Automated Setup
A PowerShell script is now included to automatically set up the desktop shortcut:

1. After completing steps 1-5 from the Manual Setup:
2. Right-click on `setup.ps1` in the project directory
3. Select "Run with PowerShell"

If you receive an execution policy error:
1. Open PowerShell as Administrator
2. Run the script with this command:
   ```
   PowerShell -ExecutionPolicy Bypass -File "path\to\setup.ps1"
   ```

The setup script will:
- Create a desktop shortcut named "Post LIC Receipt"
- Set the shortcut icon to "mail.ico" (if present in the project directory)
- Configure the proper working directory

## Usage
* Before running the program, ensure your printer/scanner is switched on and connected to the computer
* Double-click the "Post LIC Receipt" shortcut on your desktop (or open `postit.cmd`)
* The web interface will automatically open in your default browser
* To monitor detailed operations, check the command prompt window that opens with the Flask server
* When finished, close both the browser and the command prompt

**Note on the executable (.exe) version:**
* The older version with an executable file is deprecated and no longer maintained
* The current web-based version offers better performance and more features

# Technical Details

## Features
* Web-based interface using Flask
* Automatic scanner integration using WIA
* Image cropping with interactive UI
* PDF generation optimized for LIC post covers
* Auto-scrolling crop interface for better usability

## Source Code
The source code is fully available in this repository. Key files include:
* `app.py` - Main Flask application
* `foundation.py` - Core functionality for scanning, image processing, and printing
* `templates/` - HTML templates for the web interface
* `static/` - Static assets including the base image template

## Contributing
Currently, the project is owned and developed only by the original author. However, you are welcome to request features by creating an issue in the repository.

## Version History
* __v1.0__: Initial version - GUI using tkinter (completely deprecated)
* __v2.0__: Web version - using Flask
* __v2.1__: Enhanced cropping with auto-scroll functionality and simplified setup

# Thank You
**Do star and share this project if you find it useful!**
