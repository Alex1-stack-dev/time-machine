"""
Enhanced asset generator for Time Machine swimming meet management software.
Features realistic pool water effects and swimming-specific design elements.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import math
from pathlib import Path

COLORS = {
    'pool_blue': '#0077be',      # Main pool water
    'pool_deep': '#006699',      # Deeper water
    'lane_line': '#ffffff',      # White lane lines
    'lane_rope': '#ffdd00',      # Yellow lane rope floats
    'tile_light': '#00a0dc',     # Light pool tile
    'tile_dark': '#008bc1',      # Dark pool tile
    'text': '#ffffff',           # White text
    'text_shadow': '#000000',    # Text shadow
    'overlay': (0, 0, 0, 64)     # Semi-transparent overlay
}

def create_water_effect(width, height, ripple_density=30):
    """Create realistic swimming pool water texture with ripples"""
    base = Image.new('RGB', (width, height), COLORS['pool_blue'])
    ripple = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ripple)
    
    # Create random ripple patterns
    for _ in range(ripple_density):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(20, 100)
        opacity = random.randint(10, 40)
        
        # Draw concentric circles for ripple effect
        for r in range(size, 0, -5):
            draw.ellipse([x-r, y-r, x+r, y+r], 
                        fill=(255, 255, 255, int(opacity * (r/size))))
    
    # Apply gaussian blur to smooth ripples
    ripple = ripple.filter(ImageFilter.GaussianBlur(radius=3))
    
    # Blend ripples with base water
    return Image.alpha_composite(base.convert('RGBA'), ripple)

def create_lane_lines(width, height, lanes=8):
    """Create realistic swimming lane lines with floats"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    lane_height = height / lanes
    float_spacing = 30  # Distance between lane rope floats
    
    for lane in range(lanes + 1):
        y = lane * lane_height
        
        # Draw the main lane line
        draw.line([(0, y), (width, y)], fill=COLORS['lane_line'], width=2)
        
        # Add lane rope floats
        if lane < lanes:  # Don't add floats on the bottom line
            for x in range(0, width, float_spacing):
                # Alternate yellow and red floats (common in competition pools)
                float_color = COLORS['lane_rope'] if (x//float_spacing) % 2 == 0 else '#ff4444'
                draw.ellipse([x-5, y-5, x+5, y+5], fill=float_color)
    
    return img

def create_pool_tiles(width, height):
    """Create pool tile pattern for edges"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    tile_size = 20
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            color = COLORS['tile_light'] if (x+y)//tile_size % 2 == 0 else COLORS['tile_dark']
            draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=color)
    
    return img

def add_text_with_shadow(draw, text, position, font, color=COLORS['text']):
    """Add text with a subtle shadow for better readability"""
    x, y = position
    # Draw shadow
    draw.text((x+2, y+2), text, font=font, fill=COLORS['text_shadow'])
    # Draw main text
    draw.text((x, y), text, font=font, fill=color)

def create_splash():
    """Create enhanced 512x256 splash screen with realistic pool effects"""
    # Create base water effect
    img = create_water_effect(512, 256)
    
    # Add lane lines
    lanes = create_lane_lines(512, 256)
    img = Image.alpha_composite(img.convert('RGBA'), lanes)
    
    # Add pool tiles at top
    tiles = create_pool_tiles(512, 40)
    img.paste(tiles, (0, 0), tiles)
    
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        ver_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        ver_font = ImageFont.load_default()
    
    # Add title with shadow
    title = "Time Machine"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    add_text_with_shadow(draw, title, 
                        ((512 - title_width) / 2, 90),
                        title_font)
    
    # Add subtitle
    subtitle = "Professional Meet Management"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=ver_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    add_text_with_shadow(draw, subtitle,
                        ((512 - subtitle_width) / 2, 150),
                        ver_font)
    
    # Add version
    version = "v0.1.0"
    ver_bbox = draw.textbbox((0, 0), version, font=ver_font)
    ver_width = ver_bbox[2] - ver_bbox[0]
    add_text_with_shadow(draw, version,
                        (512 - ver_width - 10, 256 - 26),
                        ver_font)
    
    return img

def create_dialog():
    """Create enhanced 493x312 installer dialog"""
    # Create base with water effect
    img = create_water_effect(493, 312)
    
    # Add lane lines
    lanes = create_lane_lines(493, 312, lanes=6)
    img = Image.alpha_composite(img.convert('RGBA'), lanes)
    
    # Add pool tiles at top and sides
    top_tiles = create_pool_tiles(493, 30)
    side_tiles = create_pool_tiles(30, 312)
    
    img.paste(top_tiles, (0, 0), top_tiles)
    img.paste(side_tiles, (0, 0), side_tiles)
    img.paste(side_tiles, (463, 0), side_tiles)
    
    # Add semi-transparent overlay for text readability
    overlay = Image.new('RGBA', (493, 312), COLORS['overlay'])
    img = Image.alpha_composite(img, overlay)
    
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        text_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Add welcome text with shadow
    add_text_with_shadow(draw, "Welcome to Time Machine",
                        (40, 40), title_font)
    
    # Add description
    description = """
    Professional Meet Management Software
    
    • Streamlined event organization
    • Real-time results and timing
    • Lane assignment and heat management
    • Comprehensive athlete database
    • Meet records and statistics
    • Automated updates
    
    Get ready for your next meet!
    """
    add_text_with_shadow(draw, description,
                        (40, 100), text_font)
    
    return img

def create_banner():
    """Create enhanced 493x58 installer banner"""
    # Create water effect background
    img = create_water_effect(493, 58)
    
    # Add pool tiles at top
    tiles = create_pool_tiles(493, 10)
    img.paste(tiles, (0, 0), tiles)
    
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Add product name with shadow
    add_text_with_shadow(draw, "Time Machine - Meet Management",
                        (20, 15), font)
    
    return img

def create_icon(size):
    """Create enhanced stopwatch icon with swimming theme"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create circular pool background
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin],
                 fill=COLORS['pool_blue'])
    
    # Add lane line across center
    line_y = size // 2
    draw.line([(margin, line_y), (size-margin, line_y)],
             fill=COLORS['lane_line'], width=max(1, size//32))
    
    # Add lane rope floats
    float_size = max(1, size//32)
    for x in range(margin, size-margin, float_size*4):
        draw.ellipse([x-float_size, line_y-float_size,
                     x+float_size, line_y+float_size],
                     fill=COLORS['lane_rope'])
    
    return img

def main():
    # Ensure output directories exist
    Path("assets").mkdir(exist_ok=True)
    Path("installer/wix").mkdir(parents=True, exist_ok=True)
    
    # Create and save all assets
    print("Generating assets...")
    
    # Icon (multiple sizes)
    print("Creating icon...")
    sizes = [16, 32, 48, 256]
    icons = [create_icon(size) for size in sizes]
    icons[0].save('assets/icon.ico',
                 format='ICO',
                 sizes=[(s,s) for s in sizes])
    
    # Splash screen
    print("Creating splash screen...")
    create_splash().save('assets/splash.png')
    
    # Installer assets
    print("Creating installer assets...")
    create_banner().save('installer/wix/banner.bmp')
    create_dialog().save('installer/wix/dialog.bmp')
    
    print("Asset generation complete!")

if __name__ == '__main__':
    main()
