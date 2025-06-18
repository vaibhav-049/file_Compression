from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import compression modules
from All_compression.huffman_compression import compress_file as compress_text
from All_compression.huffman_decompress import decompress_file as decompress_text
from All_compression.image_compressor import compress_image_file as compress_image
from All_compression.pdf_compressor import compress_pdf_file as compress_pdf
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {
    'compress': {
        'text': {'txt', 'csv', 'log', 'html', 'xml'},
        'image': {'jpg', 'jpeg', 'png', 'gif', 'bmp'},
        'pdf': {'pdf'}
    },
    'decompress': {'huff'}
}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
def get_file_size(filepath):
    """Get the size of a file in bytes."""
    return os.path.getsize(filepath) if os.path.exists(filepath) else 0
def cleanup_file(filepath):
    """Safely delete a file if it exists."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    compression_type = request.form.get('type', 'text')
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_path = None
    try:
        file.save(input_path)
        if not os.path.exists(input_path):
            return jsonify({'error': 'Failed to save uploaded file'}), 500
        original_size = get_file_size(input_path)
        if compression_type == 'text':
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{name}.huff")
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    f.read()
            except UnicodeDecodeError:
                raise Exception("Invalid text file format")
            compress_text(input_path)
            if not os.path.exists(output_path):
                raise Exception("Compression failed: Output file was not created")
            compressed_size = get_file_size(output_path)
            if compressed_size == 0:
                raise Exception("Compression failed: Output file is empty")
        elif compression_type == 'image':
            quality = int(request.form.get('quality', 85))
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{name}_compressed.png")
            compress_image(input_path, output_path, quality)
            compressed_size = get_file_size(output_path)     
        elif compression_type == 'pdf':
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{name}_compressed.pdf")
            compress_pdf(input_path, output_path)
            compressed_size = get_file_size(output_path)     
        else:
            cleanup_file(input_path)
            return jsonify({'error': 'Invalid compression type'}), 400
        compression_ratio = ((original_size - compressed_size) / original_size) * 100
        return jsonify({
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'download_url': f'/download/{os.path.basename(output_path)}'
        })
    except Exception as e:
        cleanup_file(input_path)
        if output_path:
            cleanup_file(output_path)
        return jsonify({'error': str(e)}), 500
@app.route('/decompress', methods=['POST'])
def decompress():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(input_path)
        if not os.path.exists(input_path):
            return jsonify({'error': 'Failed to save uploaded file'}), 500
        compressed_size = get_file_size(input_path)
        if not filename.lower().endswith('.huff'):
            raise Exception("Only .huff files can be decompressed")
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename[:-5])
        decompress_text(input_path)
        if not os.path.exists(output_path):
            raise Exception("Decompression failed: Output file was not created")
        original_size = get_file_size(output_path)
        if original_size == 0:
            raise Exception("Decompression failed: Output file is empty")
        compression_ratio = ((compressed_size - original_size) / compressed_size) * 100
        return jsonify({
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'download_url': f'/download/{os.path.basename(output_path)}'
        })
    except Exception as e:
        cleanup_file(input_path)
        if 'output_path' in locals():
            cleanup_file(output_path)
        return jsonify({'error': str(e)}), 500
@app.route('/download/<filename>')
def download(filename):
    """Download a file from the uploads folder."""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)