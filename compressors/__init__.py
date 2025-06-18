from .huffman_compression import compress_file as compress_text
from .huffman_decompress import decompress_file as decompress_text
from .image_compressor import compress_image_file as compress_image
from .pdf_compressor import compress_pdf_file as compress_pdf

__all__ = ['compress_text', 'decompress_text', 'compress_image', 'compress_pdf']
