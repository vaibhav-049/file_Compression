import os
import pickle
class HuffmanDecompressor:
    def __init__(self):
        self.reverse_codes = {}
        self.encoded_text = ""
    def remove_padding(self, bit_string):
        padded_info = bit_string[:8]
        padding_length = int(padded_info, 2)
        actual_text = bit_string[8:-padding_length]
        return actual_text
    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_text += self.reverse_codes[current_code]
                current_code = ""
        return decoded_text
    def get_bit_string(self, byte_array):
        bit_string = ""
        for byte in byte_array:
            binary = format(byte, '08b')
            bit_string += binary
        return bit_string
    def decompress(self, input_path, output_path):
        with open(input_path, 'rb') as file:
            byte_array, self.reverse_codes = pickle.load(file)
        bit_string = self.get_bit_string(byte_array)
        encoded_text = self.remove_padding(bit_string)
        decompressed_text = self.decode_text(encoded_text)
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decompressed_text)
        return os.path.getsize(input_path), os.path.getsize(output_path)
def decompress_file(input_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")
    if not input_path.lower().endswith('.huff'):
        raise ValueError("Input file must have .huff extension")
    output_path = input_path[:-5]
    huffman = HuffmanDecompressor()
    compressed_size, decompressed_size = huffman.decompress(input_path, output_path)
    print(f"Decompression completed successfully!")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Decompressed size: {decompressed_size} bytes")
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python huffman_decompress.py <input_file.huff>")
        sys.exit(1)
    input_file = sys.argv[1]
    try:
        decompress_file(input_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
