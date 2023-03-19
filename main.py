import os
from pathlib import Path
from datetime import datetime
import qrcode
from PIL import Image, ImageDraw, ImageFont

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Wifi credentials
ssid = "WIFI_NAME"
security_protocol = "WPA;WPA2"
password = "WIFI_PASS"

# Text
text1 = "WIFI NETWORK"
text2 = "SCAN QR"

credentials = f"""
    NETWORK: {ssid}
    PASSWORD: {password}
"""

# footer
footer = """
    IT Division
    PHONE:10080-5555
"""

law = """
    LEY 26.388 - CODIGO PENAL
    Artículo 153 bis: Será reprimido con prisión de quince (15) días a seis (6) meses, si no resultare un delito
    más severamente penado, el que a sabiendas accediere por cualquier medio, sin la debida autorización o 
    excediendo la que posea, a un sistema o dato informático de acceso restringido.
"""

# Wifi info generate
wifi_info = f"WIFI:S:{ssid};T:{security_protocol};P:{password};;"

# QR code generate
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=50, border=4)
qr.add_data(wifi_info)
qr.make(fit=True)
img_qr = qr.make_image(fill_color="black", back_color="white")

# insert logo
logo = Image.open(os.path.join(BASE_DIR, "qr/image/logo.png"))

# logo size define
logo_size = 350

# get original dimensions of image
width_original, height_original = logo.size

# Calculate the new width keeping the original ratio
ratio = logo_size / height_original
new_width = int(width_original * ratio)

# resize image
resized_image = logo.resize((new_width, logo_size))

img_qr.paste(resized_image, (img_qr.size[0] // 2 - resized_image.size[0] // 2, img_qr.size[1] // 2 - resized_image.size[1] // 2))

# draw border on QR
qr_draw = ImageDraw.Draw(img_qr)
border_width = 40
border_coords = (border_width+90, border_width+90, (img_qr.size[0]-border_width)-90, (img_qr.size[1]-border_width)-90)
qr_draw.rectangle(border_coords, outline="black", width=border_width)

# Create the A4 image
a4_width = 2480
a4_height = 3508
img_a4 = Image.new("RGB", (a4_width, a4_height), color=(255, 255, 255))

# Insert the QR code in the center
img_a4.paste(img_qr, (img_a4.size[0] // 2 - img_qr.size[0] // 2, img_a4.size[1] // 6 - img_qr.size[1] // 6))

# add text
font = ImageFont.truetype(os.path.join(BASE_DIR, "qr/fonts/Audiowide-Regular.ttf"), 200)
credentials_font = ImageFont.truetype(os.path.join(BASE_DIR, "qr/fonts/Arial.ttf"), 40)
footer_font = ImageFont.truetype(os.path.join(BASE_DIR, "qr/fonts/Arial.ttf"), 50)
bar_code_font = ImageFont.truetype(os.path.join(BASE_DIR, "qr/fonts/LibreBarcode39-Regular.ttf"), 80)
law_font = ImageFont.truetype(os.path.join(BASE_DIR, "qr/fonts/Arial.ttf"), 40)

draw = ImageDraw.Draw(img_a4)

text1_width, text1_height = draw.textsize(text1, font)
text2_width, text2_height = draw.textsize(text2, font)
credentials_width, credentials_height = draw.textsize(credentials, credentials_font)

x1 = (a4_width - text1_width) // 2
y1 = (a4_height - text1_height) // 2

x2 = (a4_width - text2_width) // 2
y2 = (a4_height - text2_height) // 2

x_credentials = (a4_width - credentials_width) // 2
y_credentials = (a4_height - credentials_height) // 2

draw.text((x1, 100), text1, fill=(0, 0, 0), font=font)
draw.text((x2, 2100), text2, fill=(0, 0, 0), font=font)
draw.text((x_credentials, 1990), credentials, fill=(0, 0, 0), font=credentials_font)
draw.text((50, 3220), footer, fill=(0, 0, 0), font=footer_font, anchor="ld")

# date bar code
now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H-%M-%S")
draw.text((100, 3220), current_time, fill=(0, 0, 0), font=bar_code_font, anchor="lm")

# penal code law
draw.text((50, 3450), law, fill=(0, 0, 0), font=law_font, anchor="ld")

# black border on sheet
border_width = 20
border_coords = (border_width, border_width, a4_width-border_width, a4_height-border_width)
draw.rectangle(border_coords, outline="black", width=border_width)

# Save image
img_a4.save(os.path.join(BASE_DIR, "qr/qr_codes/qr_wifi.png"))