import os
from pathlib import Path
from datetime import datetime
import qrcode
from PIL import Image, ImageDraw, ImageFont

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure the save directory exists
save_dir = Path("qr/qr_codes")
save_dir.mkdir(parents=True, exist_ok=True)

# Wifi credentials
ssid = "Fly&Learning"
security_protocol = "WPA;WPA2"
password = "NimbusDream&Fly25"

# Text
text1 = "WIFI NETWORK"
text2 = "SCAN QR"

credentials = f"""
    NETWORK: {ssid}
    PASSWORD: {password}
"""

# Footer
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
img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

# Remove transparency and set white background
if img_qr.mode == "RGBA":
    img_qr_without_transparency = Image.new("RGB", img_qr.size, (255, 255, 255))  # White background
    img_qr_without_transparency.paste(img_qr, mask=img_qr.split()[3])  # Paste QR code without transparency
    img_qr = img_qr_without_transparency  # Replace img_qr with non-transparent version

# Insert logo
logo_path = "image/logo.png"  # Ensure path is correct
logo = Image.open(logo_path).convert("RGBA")  # Open logo

# Logo size define
logo_size = 350

# Get original dimensions of image
width_original, height_original = logo.size

# Calculate the new width keeping the original ratio
ratio = logo_size / height_original
new_width = int(width_original * ratio)

# Resize image
resized_image = logo.resize((new_width, logo_size))

# Remove transparency from logo
if resized_image.mode == "RGBA":
    logo_without_transparency = Image.new("RGB", resized_image.size, (255, 255, 255))
    logo_without_transparency.paste(resized_image, mask=resized_image.split()[3])
    resized_image = logo_without_transparency

# Paste logo in QR code
img_qr.paste(resized_image, (img_qr.size[0] // 2 - resized_image.size[0] // 2, img_qr.size[1] // 2 - resized_image.size[1] // 2))

# Draw border on QR
qr_draw = ImageDraw.Draw(img_qr)
border_width = 40
border_coords = (border_width+90, border_width+90, (img_qr.size[0]-border_width)-90, (img_qr.size[1]-border_width)-90)
qr_draw.rectangle(border_coords, outline="black", width=border_width)

# Create the A4 image
a4_width = 2480
a4_height = 3508
img_a4 = Image.new("RGB", (a4_width, a4_height), color=(255, 255, 255))

# Insert the QR code in the center
qr_x = (img_a4.size[0] - img_qr.size[0]) // 2
qr_y = (img_a4.size[1] - img_qr.size[1]) // 6
img_a4.paste(img_qr, (qr_x, qr_y))

# Add text font
font = ImageFont.truetype("fonts/Audiowide-Regular.ttf", 200)
credentials_font = ImageFont.truetype("fonts/Arial.ttf", 40)
footer_font = ImageFont.truetype("fonts/Arial.ttf", 50)
bar_code_font = ImageFont.truetype("fonts/LibreBarcode39-Regular.ttf", 80)
law_font = ImageFont.truetype("fonts/Arial.ttf", 40)

# Add text
draw = ImageDraw.Draw(img_a4)

text1_width, text1_height = draw.textbbox((0, 0), text1, font=font)[2:]
text2_width, text2_height = draw.textbbox((0, 0), text2, font=font)[2:]
credentials_width, credentials_height = draw.textbbox((0, 0), credentials, credentials_font)[2:]

# Text coordinates
x = img_a4.size[0] // 2  # Center x
y = qr_y + img_qr.size[1] + 50

draw.text((x, 100), text1, fill=(0, 0, 0), font=font, anchor="ma")
draw.text(((x, y)), text2, fill=(0, 0, 0), font=font, anchor="ma")
draw.text((x, y), credentials, fill=(0, 0, 0), font=credentials_font, anchor="md")
draw.text((50, 3220), footer, fill=(0, 0, 0), font=footer_font, anchor="ld")

# Date barcode
now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H-%M-%S")
draw.text((100, 3220), current_time, fill=(0, 0, 0), font=bar_code_font, anchor="lm")

# Penal code law
draw.text((50, 3450), law, fill=(0, 0, 0), font=law_font, anchor="ld")

# Black border on sheet
border_width = 20
border_coords = (border_width, border_width, a4_width-border_width, a4_height-border_width)
draw.rectangle(border_coords, outline="black", width=border_width)

# Save image
img_a4.save(save_dir / "qr_wifi.png")
