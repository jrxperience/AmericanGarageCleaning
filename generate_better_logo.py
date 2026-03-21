from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_advanced_mark(size=256, filepath="src/images/agc-mark-64.png", bg_color=None):
    """
    Creates an advanced circular brand mark.
    """
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    brand_blue = (0, 102, 204, 255) # #0066cc
    brand_dark = (0, 91, 181, 255)  # #005bb5
    white = (255, 255, 255, 255)
    red = (204, 0, 0, 255)          # Accent red for "American"

    if bg_color:
        draw.ellipse([0, 0, size, size], fill=bg_color)
    else:
        # Draw base circle
        margin = int(size * 0.05)
        draw.ellipse([margin, margin, size - margin, size - margin], fill=brand_blue)

        # Draw a slightly smaller circle for depth
        inner_margin = int(size * 0.12)
        draw.ellipse([inner_margin, inner_margin, size - inner_margin, size - inner_margin], fill=brand_dark)

    # We will try to load a font, otherwise fallback
    font_size = int(size * 0.45)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Draw 'A'
    text = "A"
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size - w) / 2 - (size*0.12), (size - h) / 2 - (size*0.08)), text, font=font, fill=white)

    # Draw 'C'
    text = "C"
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size - w) / 2 + (size*0.18), (size - h) / 2 + (size*0.12)), text, font=font, fill=white)

    # Draw star in mark
    cx, cy = size/2, size*0.18
    outer_r = size * 0.12
    inner_r = size * 0.05
    star_points = []
    points = 5
    for i in range(points * 2):
        angle = i * math.pi / points - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        star_points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(star_points, fill=red)

    # Save image
    img.save(filepath, "PNG")
    print(f"Created {filepath}")

def create_advanced_logo(width=800, height=200, filepath="src/images/agc-logo.png"):
    """
    Creates a full rectangular logo with the mark and text.
    """
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    brand_blue = (0, 102, 204, 255)
    steel = (200, 200, 200, 255)
    white = (255, 255, 255, 255)
    red = (204, 0, 0, 255)

    # Create the mark separately and paste it
    mark_size = int(height * 0.8)
    mark_img = Image.new("RGBA", (mark_size, mark_size), (255, 255, 255, 0))
    mark_draw = ImageDraw.Draw(mark_img)

    # Draw Mark
    margin = int(mark_size * 0.05)
    mark_draw.ellipse([margin, margin, mark_size - margin, mark_size - margin], fill=brand_blue)
    inner_margin = int(mark_size * 0.12)
    mark_draw.ellipse([inner_margin, inner_margin, mark_size - inner_margin, mark_size - inner_margin], fill=(0, 91, 181, 255))

    try:
        font_mark = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(mark_size * 0.45))
    except IOError:
        font_mark = ImageFont.load_default()

    text = "A"
    bbox = mark_draw.textbbox((0, 0), text, font=font_mark)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    mark_draw.text(((mark_size - w) / 2 - (mark_size*0.12), (mark_size - h) / 2 - (mark_size*0.08)), text, font=font_mark, fill=white)

    text = "C"
    bbox = mark_draw.textbbox((0, 0), text, font=font_mark)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    mark_draw.text(((mark_size - w) / 2 + (mark_size*0.18), (mark_size - h) / 2 + (mark_size*0.12)), text, font=font_mark, fill=white)

    # Draw star in mark
    cx, cy = mark_size/2, mark_size*0.18
    outer_r = mark_size * 0.12
    inner_r = mark_size * 0.05
    star_points = []
    points = 5
    for i in range(points * 2):
        angle = i * math.pi / points - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        star_points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    mark_draw.polygon(star_points, fill=red)

    # Paste mark into logo
    mark_y = (height - mark_size) // 2
    img.paste(mark_img, (20, mark_y), mark_img)

    # Draw Text
    text_x = mark_size + 50

    try:
        font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(height * 0.35))
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(height * 0.18))
    except IOError:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Draw Main Text
    draw.text((text_x, height * 0.25), "American ", font=font_main, fill=red)

    bbox = draw.textbbox((0, 0), "American ", font=font_main)
    w1 = bbox[2] - bbox[0]
    draw.text((text_x + w1, height * 0.25), "Garage Cleaning", font=font_main, fill=white)

    # Draw Sub Text
    draw.text((text_x + 5, height * 0.65), "COMMERCIAL MAINTENANCE", font=font_sub, fill=steel)

    # Crop transparent borders roughly for better usage
    bbox = img.getbbox()
    if bbox:
        img = img.crop((0, 0, bbox[2] + 20, height))

    img.save(filepath, "PNG")
    print(f"Created {filepath}")

if __name__ == "__main__":
    os.makedirs("src/images", exist_ok=True)
    create_advanced_mark(size=256, filepath="src/images/agc-mark-64.png")
    create_advanced_logo(width=800, height=200, filepath="src/images/agc-logo.png")
