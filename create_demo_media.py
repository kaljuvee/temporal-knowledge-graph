#!/usr/bin/env python3
"""
Create demo media (GIF and video) from Streamlit interface screenshots
"""

import imageio
from PIL import Image, ImageDraw, ImageFont
import os
import glob

def create_demo_gif():
    """Create animated GIF from screenshots"""
    
    # Find all interface screenshots
    screenshot_files = sorted(glob.glob("streamlit_interface_*.png"))
    
    if not screenshot_files:
        print("No screenshot files found!")
        return
    
    print(f"Found {len(screenshot_files)} screenshots")
    
    # Load and resize images to consistent size
    images = []
    target_width = 800
    target_height = 600  # Fixed height for consistency
    
    for i, filename in enumerate(screenshot_files):
        print(f"Processing {filename}...")
        
        # Load image
        img = Image.open(filename)
        
        # Resize image to exact target size
        img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Add title overlay
        draw = ImageDraw.Draw(img_resized)
        
        # Try to load a font, fall back to default if not available
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        titles = [
            "🧠 Temporal Knowledge Graph Demo",
            "➕ Adding Content to Knowledge Graph", 
            "🔍 Query & Search Interface",
            "📊 Analytics Dashboard",
            "📚 Comprehensive User Guide"
        ]
        
        if i < len(titles):
            title = titles[i]
            
            # Get text bounding box
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position text at top center
            x = (target_width - text_width) // 2
            y = 20
            
            # Draw background rectangle for text
            padding = 10
            draw.rectangle([x-padding, y-padding, x+text_width+padding, y+text_height+padding], 
                         fill=(0, 0, 0, 180))
            
            # Draw text
            draw.text((x, y), title, fill=(255, 255, 255), font=font)
        
        # Convert to numpy array for imageio
        import numpy as np
        images.append(np.array(img_resized))
    
    # Create animated GIF
    print("Creating animated GIF...")
    imageio.mimsave('demo_preview.gif', images, duration=2.5, loop=0)
    print("✅ Created demo_preview.gif")
    
    # Create a longer duration video-style GIF
    print("Creating video-style GIF...")
    video_images = []
    for img in images:
        # Add each frame multiple times for longer duration
        for _ in range(8):  # 8 frames * 0.3s = 2.4s per slide
            video_images.append(img)
    
    imageio.mimsave('demo_walkthrough.gif', video_images, duration=0.3, loop=0)
    print("✅ Created demo_walkthrough.gif")

def create_demo_video():
    """Create MP4 video from screenshots"""
    
    screenshot_files = sorted(glob.glob("streamlit_interface_*.png"))
    
    if not screenshot_files:
        print("No screenshot files found!")
        return
    
    print(f"Creating video from {len(screenshot_files)} screenshots")
    
    # Load and process images to consistent size
    images = []
    target_width = 1200
    target_height = 900  # Fixed height for consistency
    
    for i, filename in enumerate(screenshot_files):
        print(f"Processing {filename} for video...")
        
        # Load image
        img = Image.open(filename)
        
        # Resize image to exact target size
        img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Add title and description overlay
        draw = ImageDraw.Draw(img_resized)
        
        # Try to load fonts
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
            desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            title_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()
        
        titles = [
            "🧠 Temporal Knowledge Graph Demo",
            "➕ Adding Content to Knowledge Graph", 
            "🔍 Query & Search Interface",
            "📊 Analytics Dashboard",
            "📚 Comprehensive User Guide"
        ]
        
        descriptions = [
            "Based on OpenAI Cookbook - Track information changes over time",
            "Process individual statements or entire documents with AI",
            "Ask natural language questions about temporal relationships",
            "Visualize knowledge graph composition and temporal events",
            "Complete documentation with examples and best practices"
        ]
        
        if i < len(titles):
            title = titles[i]
            desc = descriptions[i] if i < len(descriptions) else ""
            
            # Title
            bbox = draw.textbbox((0, 0), title, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (target_width - text_width) // 2
            y = 30
            
            # Background for title
            padding = 15
            draw.rectangle([x-padding, y-padding, x+text_width+padding, y+text_height+padding], 
                         fill=(0, 0, 0, 200))
            draw.text((x, y), title, fill=(255, 255, 255), font=title_font)
            
            # Description
            if desc:
                bbox = draw.textbbox((0, 0), desc, font=desc_font)
                desc_width = bbox[2] - bbox[0]
                desc_height = bbox[3] - bbox[1]
                
                x_desc = (target_width - desc_width) // 2
                y_desc = y + text_height + 20
                
                # Background for description
                draw.rectangle([x_desc-padding, y_desc-5, x_desc+desc_width+padding, y_desc+desc_height+5], 
                             fill=(0, 0, 0, 150))
                draw.text((x_desc, y_desc), desc, fill=(255, 255, 255), font=desc_font)
        
        # Convert to numpy array for imageio
        import numpy as np
        images.append(np.array(img_resized))
    
    # Create video frames (repeat each image for duration)
    video_frames = []
    for img in images:
        # Add each frame 75 times (3 seconds at 25 fps)
        for _ in range(75):
            video_frames.append(img)
    
    # Save as MP4
    print("Creating MP4 video...")
    imageio.mimsave('demo_walkthrough.mp4', video_frames, fps=25, quality=8)
    print("✅ Created demo_walkthrough.mp4")

if __name__ == "__main__":
    print("🎬 Creating demo media from screenshots...")
    
    # Check if we have screenshots
    screenshots = glob.glob("streamlit_interface_*.png")
    if not screenshots:
        print("❌ No screenshots found! Please run the browser capture first.")
        exit(1)
    
    print(f"📸 Found {len(screenshots)} screenshots")
    
    # Create both GIF and video
    create_demo_gif()
    create_demo_video()
    
    print("\n🎉 Demo media creation complete!")
    print("📁 Files created:")
    print("   - demo_preview.gif (short animated preview)")
    print("   - demo_walkthrough.gif (longer walkthrough)")
    print("   - demo_walkthrough.mp4 (video format)")

