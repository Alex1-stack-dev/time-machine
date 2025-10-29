"""
Asset generator for Time Machine installer.
Creates:
- icon.ico: Multi-resolution Windows icon (16,32,48,256)
- splash.png: 512x256 splash screen
- banner.bmp: 493x58 installer header
- dialog.bmp: 493x312 installer welcome screen

Uses PIL/Pillow for image generation.
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Colors inspired by professional sports timing software
COLORS = {
    'primary': '#003366',  # Deep blue
    'secondary': '#0066cc', # Bright blue
    'accent': '#ffffff',   # White
    'text': '#000000'      # Black
}

def create_icon(size):
    """Create a simple, professional stopwatch icon"""
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # Draw a circular stopwatch shape
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=COLORS['primary'],
                 outline=COLORS['secondary'])
    
    # Add timing marks
    center = size // 2
    for i in range(12):
        angle = i * 30  # 360/12
        # Draw timing marks...
        
    return img

def create_splash():
    """Create 512x256 splash screen"""
    img = Image.new('RGB', (512, 256), COLORS['primary'])
    draw = ImageDraw.Draw(img)
    
    # Add "Time Machine" text
    # Add version number
    # Add subtle timing grid background
    
    return img

def create_banner():
    """Create 493x58 installer banner"""
    img = Image.new('RGB', (493, 58), COLORS['primary'])
    draw = ImageDraw.Draw(img)
    
    # Add product name
    # Add subtle professional accent graphics
    
    return img

def create_dialog():
    """Create 493x312 installer dialog"""
    img = Image.new('RGB', (493, 312), COLORS['accent'])
    draw = ImageDraw.Draw(img)
    
    # Add welcome text
    # Add product description
    # Add professional timing imagery
    
    return img

def main():
    # Create icon in multiple sizes
    sizes = [16, 32, 48, 256]
    icons = []
    for size in sizes:
        icons.append(create_icon(size))
    
    # Save multi-size icon
    icons[0].save('icon.ico', 
                 format='ICO',
                 sizes=[(s,s) for s in sizes])
    
    # Save other assets
    create_splash().save('splash.png')
    create_banner().save('installer/wix/banner.bmp')
    create_dialog().save('installer/wix/dialog.bmp')

if __name__ == '__main__':
    main()
