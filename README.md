WiFi QR Code Generator

This is a simple Python script that generates a QR code for a WiFi network, containing the network name and password. The code can be easily scanned by any QR code reader to join the network without having to manually enter the details.

Installation

Clone this repository or download the zip file and extract it to your desired location.
Make sure you have Python 3 installed on your system.
Install the required packages by running pip install -r requirements.txt in the project directory.

Usage

Open wifi_qr_generator.py in a text editor.
Modify the ssid and password variables to match the name and password of your WiFi network.
Run the script using python wifi_qr_generator.py.
The script will generate a QR code as a PNG image in the same directory as the script.
Dependencies
This script uses the qrcode and Pillow libraries to generate and save the QR code image. These libraries are included in the requirements.txt file and can be installed using pip.

Example
Here is an example QR code generated by the script:

Example QR code

This QR code contains the details of a WiFi network with the name "MyNetwork" and password "MyPassword". When scanned by a QR code reader, the user will be prompted to join the network.