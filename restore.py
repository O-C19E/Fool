import hashlib
import os
import random
import struct
import subprocess
import tempfile
import sys

BLOCK_SIZE = 1024

def get_seed_from_key(key: str) -> int:
    return int(hashlib.sha256(key.encode()).hexdigest(), 16)

def generate_permutation(length: int, key: str):
    rng = random.Random(get_seed_from_key(key))
    indices = list(range(length))
    rng.shuffle(indices)
    return indices

def split_blocks(data: bytes):
    return [data[i : i + BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

def restore_and_execute(scrambled_exe, key):
    with open(scrambled_exe, "rb") as f:
        original_size = struct.unpack(">Q", f.read(8))[0]
        data = f.read()

    blocks = split_blocks(data)
    permutation = generate_permutation(len(blocks), key)
    restored_blocks = [None] * len(blocks)
    for i, perm_index in enumerate(permutation):
        restored_blocks[perm_index] = blocks[i]
    restored_data = b"".join(restored_blocks)
    restored_data = restored_data[:original_size]
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "syscache_tmp.exe")
    with open(temp_path, "wb") as f:
        f.write(restored_data)

    os.chmod(temp_path, 0o775)
    subprocess.Popen(temp_path, shell=True)
    print("[+] Protected program launched")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 launcher.py <scrambled.exe>")
        sys.exit(1)

    scrambled_file = sys.argv[1]
    KEY = input("Product Key: ")
    restore_and_execute(scrambled_file, KEY)
