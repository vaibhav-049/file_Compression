import os
import sys
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Warning: PyMuPDF not available. Using basic PDF compression only.")
    fitz = None
import io
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
class PDFCompressor:
    def __init__(self):
        self.compression_level = 9  
        self.image_quality = 60  
        self.max_image_size = 1600  
        self.min_size_to_compress = 100 * 1024  
    def compress_image(self, image_data):
        """Compress an image while maintaining reasonable quality"""
        try:
            img = Image.open(io.BytesIO(image_data))
            if img.mode in ['RGBA', 'P']:
                img = img.convert('RGB')
            if max(img.size) > self.max_image_size:
                ratio = self.max_image_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=self.image_quality, optimize=True)
            return output.getvalue()
        except Exception:
            return image_data
    def compress_pdf(self, input_path, output_path):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        if not input_path.lower().endswith('.pdf'):
            raise ValueError("Input file must be a PDF")
        try:            
            temp_path = output_path + ".temp.pdf"
            if fitz:
                doc = fitz.open(input_path)
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    image_list = page.get_images()          
                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        if doc.xref_stream_raw(xref) and len(doc.xref_stream_raw(xref)) < self.min_size_to_compress:
                            continue
                        try:
                            image_data = doc.extract_image(xref)
                            if image_data and image_data["image"]:
                                compressed_data = self.compress_image(image_data["image"])
                                if len(compressed_data) < len(image_data["image"]):
                                    doc.update_stream(xref, compressed_data)
                        except Exception:
                            continue         
                doc.save(temp_path, garbage=4, deflate=True, clean=True)
                doc.close()
            else:
                with open(input_path, 'rb') as src, open(temp_path, 'wb') as dst:
                    dst.write(src.read())
            reader = PdfReader(temp_path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.compress_content_streams = True
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            try:
                os.remove(temp_path)
            except:
                pass
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            if compressed_size >= original_size:
                with open(input_path, 'rb') as src, open(output_path, 'wb') as dst:
                    dst.write(src.read())
                compressed_size = original_size
            compression_ratio = (1 - compressed_size/original_size) * 100
            return {
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'pages': len(reader.pages)
            }
        except Exception as e:
            raise Exception(f"Error compressing PDF: {str(e)}")
def compress_pdf_file(input_path, output_path=None):
    try:
        compressor = PDFCompressor()
        if output_path is None:
            input_name = os.path.splitext(input_path)[0]
            output_path = f"{input_name}_compressed.pdf"
        print("\nCompressing PDF...")
        stats = compressor.compress_pdf(input_path, output_path)
        print("\nCompression completed successfully!")
        print(f"Original size: {stats['original_size']:,} bytes")
        print(f"Compressed size: {stats['compressed_size']:,} bytes")
        print(f"Compression ratio: {stats['compression_ratio']:.2f}%")
        print(f"Number of pages: {stats['pages']}")
        print(f"Output saved as: {output_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
def get_readable_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python pdf_compressor.py <input_file.pdf> [output_file.pdf]")
        print("If output file is not specified, '_compressed' will be added to the input filename")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    if not input_file.lower().endswith('.pdf'):
        print("Error: Input file must be a PDF")
        sys.exit(1)
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    if output_file and os.path.exists(output_file):
        response = input(f"Output file {output_file} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled")
            sys.exit(0)
    compress_pdf_file(input_file, output_file)
