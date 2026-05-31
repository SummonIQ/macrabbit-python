#!/usr/bin/env python3
"""
Create a simple macOS-style app icon for the Service Manager app.
This creates a basic icon that can be used with the app bundle.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Create a simple app icon with a gear and settings theme."""
    
    # Create a 512x512 icon (standard macOS app icon size)
    size = 512
    icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Background circle with gradient-like effect
    center = size // 2
    radius = size // 2 - 20
    
    # Draw a rounded rectangle background (macOS style)
    rect_size = int(size * 0.8)
    rect_x = (size - rect_size) // 2
    rect_y = (size - rect_size) // 2
    corner_radius = 40
    
    # Background with subtle gradient effect
    for i in range(corner_radius):
        alpha = int(255 * (1 - i / corner_radius))
        color = (122, 122, 247, alpha)  # Blue-ish color
        draw.ellipse([rect_x + i, rect_y + i, rect_x + rect_size - i, rect_y + rect_size - i], 
                    fill=color, outline=None)
    
    # Draw a gear icon in the center
    gear_center = center
    gear_radius = int(size * 0.25)
    gear_inner_radius = int(gear_radius * 0.6)
    
    # Draw gear teeth
    num_teeth = 12
    tooth_length = int(gear_radius * 0.3)
    
    for i in range(num_teeth):
        angle = (i * 360 / num_teeth) * 3.14159 / 180
        outer_x = gear_center + int((gear_radius + tooth_length) * (angle % 1))
        outer_y = gear_center + int((gear_radius + tooth_length) * (angle % 1))
        inner_x = gear_center + int(gear_radius * (angle % 1))
        inner_y = gear_center + int(gear_radius * (angle % 1))
        
        # Draw tooth
        draw.line([(outer_x, outer_y), (inner_x, inner_y)], fill=(255, 255, 255, 255), width=8)
    
    # Draw inner circle
    draw.ellipse([gear_center - gear_inner_radius, gear_center - gear_inner_radius,
                  gear_center + gear_inner_radius, gear_center + gear_inner_radius],
                 fill=(255, 255, 255, 255), outline=None)
    
    # Draw center circle
    center_radius = int(gear_inner_radius * 0.3)
    draw.ellipse([gear_center - center_radius, gear_center - center_radius,
                  gear_center + center_radius, gear_center + center_radius],
                 fill=(122, 122, 247, 255), outline=None)
    
    # Save the icon
    icon_path = "app_icon.png"
    icon.save(icon_path, "PNG")
    print(f"Created app icon: {icon_path}")
    
    return icon_path

if __name__ == "__main__":
    try:
        create_app_icon()
    except ImportError:
        print("PIL/Pillow not installed. Installing...")
        import subprocess
        subprocess.run(["pip3", "install", "Pillow"])
        create_app_icon() 