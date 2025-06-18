import os
import heapq
from collections import defaultdict
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq
class HuffmanCompressor:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_codes = {}
    def make_frequency_dict(self, text):
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1
        return frequency
    def make_heap(self, frequency):
        for char, freq in frequency.items():
            node = Node(char, freq)
            heapq.heappush(self.heap, node)
    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)
    def make_codes_helper(self, node, current_code):
        if node is None:
            return
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_codes[current_code] = node.char
            return
        self.make_codes_helper(node.left, current_code + "0")
        self.make_codes_helper(node.right, current_code + "1")
    def make_codes(self):
        root = heapq.heappop(self.heap)
        self.make_codes_helper(root, "")
    def get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text
    def pad_encoded_text(self, encoded_text):
        padding_length = 8 - (len(encoded_text) % 8)
        for _ in range(padding_length):
            encoded_text += "0"
        padded_info = format(padding_length, "08b")
        return padded_info + encoded_text
    def get_byte_array(self, padded_text):
        array = bytearray()
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i+8]
            array.append(int(byte, 2))
        return array
    def compress(self, input_path, output_path):
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()
        encoded_text = self.get_encoded_text(text)
        padded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_text)
        with open(output_path, 'wb') as output:
            import pickle
            pickle.dump((byte_array, self.reverse_codes), output)
        return os.path.getsize(input_path), os.path.getsize(output_path)
def compress_file(input_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")
    allowed_extensions = {'.txt', '.csv', '.log', '.html', '.xml'}
    file_extension = os.path.splitext(input_path)[1].lower()
    if file_extension not in allowed_extensions:
        raise ValueError(f"Unsupported file extension. Supported extensions are: {allowed_extensions}")
    output_path = os.path.splitext(input_path)[0] + '.huff'
    huffman = HuffmanCompressor()
    original_size, compressed_size = huffman.compress(input_path, output_path)
    compression_ratio = (1 - compressed_size/original_size) * 100
    print("Compression completed successfully!")
    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {compression_ratio:.2f}%")
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python huffman_compression.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    try:
        compress_file(input_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)