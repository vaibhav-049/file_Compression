# Smart File Compressor

A powerful web application that provides efficient file compression and decompression capabilities for multiple file types. Built with Flask and modern web technologies, this application offers an intuitive interface for compressing text files, images, and PDFs.

## Features

- **Multiple File Types Support**

  - Text Files (.txt, .csv, .log, .html, .xml)
  - Images (.jpg, .jpeg, .png, .gif, .bmp)
  - PDF Documents (.pdf)

- **Advanced Compression Algorithms**

  - Huffman Compression for text files
  - Optimized image compression with quality control
  - PDF compression while maintaining readability

- **User-Friendly Interface**

  - Drag & Drop file upload
  - Multiple file selection
  - Real-time compression status
  - File type auto-detection
  - Compression ratio display

- **Bulk Operations**
  - Process multiple files simultaneously
  - Batch file removal
  - Individual file management

## Prerequisites

- Python 3.8 or higher
- Flask web framework
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd DAA_project_final
```

2. Create and activate a virtual environment (recommended):

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Project Structure

```
DAA_project_final/
├── All_compression/
│   ├── huffman_compression.py
│   ├── huffman_decompress.py
│   ├── image_compressor.py
│   ├── pdf_compressor.py
│   └── utils.py
├── static/
│   ├── additional_styles.css
│   ├── script.js
│   └── styles.css
├── templates/
│   └── index.html
├── uploads/          # Generated automatically for storing files
├── app.py           # Main Flask application
└── README.md
```

## Usage

1. Start the Flask server:

```bash
python app.py
```

2. Open a web browser and navigate to:

```
http://localhost:5000
```

3. Using the Application:
   - Select compression or decompression mode
   - Choose file type (text, image, or PDF)
   - Drag & drop files or use the browse button
   - For images, adjust quality slider if needed
   - Click "Process All Files" to start compression
   - Download processed files using the download buttons

## Compression Methods

### Text Files

- Uses Huffman coding algorithm
- Creates .huff files for compressed output
- Efficiently handles various text formats

### Images

- Quality-controlled compression
- Maintains balance between size and quality
- Supports multiple image formats

### PDFs

- Optimized PDF compression
- Preserves document quality
- Reduces file size while maintaining readability

## Features in Detail

### File Upload

- Drag & drop interface
- Multiple file selection
- File type validation
- Size limit checking (16MB per file)

### Processing

- Real-time status updates
- Progress tracking
- Error handling
- Automatic file type detection

### Results

- Compression ratio display
- Before/after size comparison
- Easy download options
- Status indicators for each file

## Error Handling

The application includes comprehensive error handling for:

- Invalid file types
- File size limits
- Processing failures
- Server errors
- Network issues

## Security Features

- Secure file handling
- Input validation
- Safe file naming
- Automatic file cleanup
- Maximum file size limits

## Browser Compatibility

Tested and compatible with:

- Google Chrome (recommended)
- Mozilla Firefox
- Microsoft Edge
- Safari

## Known Limitations

- Maximum file size: 16MB per file
- Supported file types are limited to specified extensions
- Browser-based compression for better performance

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask framework
- Huffman coding implementation
- Image processing libraries
- PDF compression tools
