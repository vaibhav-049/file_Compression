import os
import shutil
def get_file_size(file_path):
    try:
        size_bytes = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    except:
        return "N/A"
def get_file_extension(file_path):
    return os.path.splitext(file_path)[1].lower()
def is_text_file(file_path):
    return get_file_extension(file_path) in ['.txt', '.csv', '.log', '.html', '.xml']
def is_image_file(file_path):
    return get_file_extension(file_path) in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
def is_pdf_file(file_path):
    return get_file_extension(file_path) == '.pdf'
def is_huff_file(file_path):
    return get_file_extension(file_path) == '.huff'
def copy_to_working_dir(file_path, working_dir):
    os.makedirs(working_dir, exist_ok=True)
    dest_path = os.path.join(working_dir, os.path.basename(file_path))
    shutil.copy2(file_path, dest_path)
    return dest_path
