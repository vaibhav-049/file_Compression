import os
from PIL import Image
import sys
class ImageCompressor:
    def __init__(self):
        self.supported_input_formats = {'.jpg', '.jpeg', '.bmp', '.png', '.gif'}
        self.supported_output_formats = {'.png', '.jpg'}
    def get_output_format(self, output_path):
        ext = os.path.splitext(output_path)[1].lower()
        if ext not in self.supported_output_formats:
            raise ValueError(f"Unsupported output format. Supported formats are: {self.supported_output_formats}")
        return ext
    def optimize_png(self, img):
        return img.quantize(colors=256, method=2)
    def compress_image(self, input_path, output_path, quality=85):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        input_ext = os.path.splitext(input_path)[1].lower()
        if input_ext not in self.supported_input_formats:
            raise ValueError(f"Unsupported input format. Supported formats are: {self.supported_input_formats}")
        output_format = self.get_output_format(output_path)
        try:
            with Image.open(input_path) as img:
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                if output_format == '.png':
                    if input_ext != '.png':
                        img = self.optimize_png(img)
                    img.save(output_path, 'PNG', optimize=True)
                else:  # .jpg
                    img.save(output_path, 'JPEG', quality=quality, optimize=True) 
                original_size = os.path.getsize(input_path)
                compressed_size = os.path.getsize(output_path)
                compression_ratio = (1 - compressed_size/original_size) * 100         
                return {
                    'original_size': original_size,
                    'compressed_size': compressed_size,
                    'compression_ratio': compression_ratio,
                    'width': img.width,
                    'height': img.height
                }
        except Exception as e:
            raise Exception(f"Error compressing image: {str(e)}")
def compress_image_file(input_path, output_path=None, quality=85):
    try:
        compressor = ImageCompressor() 
        if output_path is None:
            input_name, input_ext = os.path.splitext(input_path)
            if input_ext.lower() in {'.jpg', '.jpeg'}:
                output_path = f"{input_name}_compressed.jpg"
            else:
                output_path = f"{input_name}_compressed.png" 
        stats = compressor.compress_image(input_path, output_path, quality)  
        print("\nCompression completed successfully!")
        print(f"Original size: {stats['original_size']:,} bytes")
        print(f"Compressed size: {stats['compressed_size']:,} bytes")
        print(f"Compression ratio: {stats['compression_ratio']:.2f}%")
        print(f"Image dimensions: {stats['width']}x{stats['height']} pixels")
        print(f"Output saved as: {output_path}")   
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python image_compressor.py <input_file> [output_file] [quality]")
        print("quality: 0-100 (default: 85, only applies to JPEG output)")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    quality = int(sys.argv[3]) if len(sys.argv) > 3 else 85
    if quality < 0 or quality > 100:
        print("Error: Quality must be between 0 and 100")
        sys.exit(1)
    compress_image_file(input_file, output_file, quality)
