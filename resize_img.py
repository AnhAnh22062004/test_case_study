from PIL import Image, ImageFilter
from pathlib import Path
import sys

def resize_image(input_path, output_path):
    """Resize 1080x1920 to 1200x1920 using edge mirroring with gaussian blur"""
    
    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    w, h = img.size
    new_w, new_h = 1200, 1920
    padding = (new_w - w) // 2
    
    # Create canvas and paste original image
    canvas = Image.new('RGB', (new_w, new_h))
    canvas.paste(img, (padding, 0))
    
    # Fill left side with mirrored + blurred edge
    left = img.crop((0, 0, 50, h))
    left = left.transpose(Image.FLIP_LEFT_RIGHT).filter(ImageFilter.GaussianBlur(15))
    canvas.paste(left.resize((padding, new_h)), (0, 0))
    
    # Fill right side with mirrored + blurred edge
    right = img.crop((w-50, 0, w, h))
    right = right.transpose(Image.FLIP_LEFT_RIGHT).filter(ImageFilter.GaussianBlur(15))
    canvas.paste(right.resize((padding, new_h)), (new_w-padding, 0))
    
    canvas.save(output_path, 'JPEG', quality=95)
    print(f"✓ {input_path.name} → {output_path.name}")


def process(input_path):
    """Process single file or entire folder"""
    
    input_path = Path(input_path)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Single file
    if input_path.is_file():
        output_path = output_dir / f"resized_{input_path.stem}.jpg"
        resize_image(input_path, output_path)
        return
    
    # Folder
    if input_path.is_dir():
        files = list(input_path.glob("*.jpg")) + list(input_path.glob("*.png"))
        if not files:
            print("No images found")
            return
        
        print(f"Processing {len(files)} images...\n")
        for img_file in files:
            output_path = output_dir / f"resized_{img_file.stem}.jpg"
            resize_image(img_file, output_path)
        
        print(f"Done! Check output/ folder")
        return
    
    print(f"Error: {input_path} not found")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python resize_1080_to_1200.py <file_or_folder>")
        print("Example: python resize_1080_to_1200.py image.jpg")
        print("Example: python resize_1080_to_1200.py input/")
        sys.exit(1)
    
    process(sys.argv[1])