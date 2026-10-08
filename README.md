# ARCore Image Tester

A simple Python GUI for quickly testing how suitable images are for **Google ARCore image tracking**.

## What is it?

**ARCore Image Tester** is a GUI tool designed to make testing images for **ARCore image tracking** faster and easier.

Instead of repeatedly using the `arcoreimg` command-line tool to check how well an image performs as an ARCore reference image, you can simply **drag and drop an image into the application** and quickly see its results.

This makes it easier to test different images and determine how suitable they are for use with ARCore image tracking without having to type commands in the terminal every time.

The tool uses `arcoreimg` in the background and provides a simple graphical interface for it.

## Requirements

- Python 3
- `arcoreimg.exe`
- The Python packages listed in `requirements.txt`

### Python Packages

The required Python packages are:

     - tkinterdnd2
     - Pillow
     
You can install them automatically with:

    pip install -r requirements.txt

## Setup

1- Download or clone this repository.

2- Make sure `arcoreimg.exe` is in the **same folder** as `ARCoreImageTester.py`.

Your folder should look similar to:

    ARCore-Image-Tester/ 
      ├── ARCoreImageTester.py 
      ├── arcoreimg.exe 
      ├── requirements.txt 
      ├── README.md 
      └── LICENSE

3- Open **Command Prompt** or **PowerShell**.

4- Navigate to the folder where you downloaded the tool.
Change the path below to your own folder:

    cd "C:\Users\YourUser\Downloads\ARCore-Image-Tester"

5- Install the required Python packages:
   
    pip install -r requirements.txt

6- Run the tool:

    python ARCoreImageTester.py

7- **Drag and drop an image into the application** to test it.

You can also use **Select Image** to choose an image manually.

## Supported Images

The tool currently supports:

- JPG
- JPEG
- PNG

## Disclaimer

**ARCore Image Tester is an independent third-party tool and is not affiliated with, endorsed by, or developed by Google.**

**ARCore** and **arcoreimg** are Google technologies and all related trademarks, technologies, and intellectual property belong to **Google LLC**.

This project provides a Python-based graphical interface for using `arcoreimg` to test and inspect images. It does not contain, modify, or recreate ARCore.