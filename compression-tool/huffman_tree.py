from heapq import heappop, heappush
from pathlib import Path

from bitstring import BitArray


class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __str__(self):
        return f"0:{str(self.left)}  1:{str(self.right)}"



class HuffmanCore:
    def __init__(self):
        self.code = {}
        self.reverse_codes = {}

    def get_freq(self, text):
        freq = {}
        for char in text:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
        return freq

    def build(self, freq):

        heap = []
        for char, freq in freq.items():
            heappush(heap, HuffmanNode(char, freq))

        while len(heap) > 1:
            left = heappop(heap)
            right = heappop(heap)
            parent = HuffmanNode(freq=left.freq + right.freq)
            parent.left = left
            parent.right = right
            heappush(heap, parent)
        return heap[0] if heap else None

    def code_generator(self, node, prefix=""):
        if node is None:
            return {}
        if node.char is not None:
            self.code[node.char] = prefix
            self.reverse_codes[prefix] = node.char
            return

        self.code_generator(node.left, prefix + "0")
        self.code_generator(node.right, prefix + "1")

    def encode(self, filename):
        try:
            with open(filename, "r") as f:
                data = f.read()

            freq = self.get_freq(data)
            root = self.build(freq)
            self.code_generator(root)

            bits = "".join(self.code[char] for char in data)
            encoded = BitArray('0b' + bits)

            output_file = filename + ".huff"
            with open(output_file, "wb") as f:
                encoded.tofile(f)

            original_size = len(data)
            compressed_size = Path(output_file).stat().st_size
            print(f"Original size: {original_size /(1024*1024):.2f} MB")
            print(f"Compressed size: {compressed_size / (1024* 1024):.2f} MB")
            print(f"Compression ratio: {compressed_size/original_size:.2%}")

        except FileNotFoundError:
            raise Exception(f"File not found: {filename}")



    def decode(self, bits):
        pass
