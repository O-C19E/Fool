import hashlib
import os
import random
import sqlite3
import string
import struct
from tkinter import filedialog

BLOCK_SIZE = 1024
DB_NAME = "licenses.db"


# -----------------------------
# RANDOM KEY GENERATOR
# -----------------------------
def generate_key():
    chars = string.ascii_uppercase + string.digits
    parts = ["".join(random.choice(chars) for _ in range(4)) for _ in range(4)]
    return "-".join(parts)


# -----------------------------
# HASH FILE
# -----------------------------
def hash_file(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


# -----------------------------
# SCRAMBLING FUNCTIONS
# -----------------------------
def get_seed_from_key(key: str) -> int:
    return int(hashlib.sha256(key.encode()).hexdigest(), 16)


def generate_permutation(length: int, key: str):
    rng = random.Random(get_seed_from_key(key))
    indices = list(range(length))
    rng.shuffle(indices)
    return indices


def pad_data(data: bytes):
    original_size = len(data)
    padding_needed = (BLOCK_SIZE - (original_size % BLOCK_SIZE)) % BLOCK_SIZE
    padded_data = data + b"\x00" * padding_needed
    return padded_data, original_size


def split_blocks(data: bytes):
    return [data[i : i + BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]


def scramble(input_path, output_path, key):

    with open(input_path, "rb") as f:
        data = f.read()

    padded_data, original_size = pad_data(data)

    blocks = split_blocks(padded_data)

    permutation = generate_permutation(len(blocks), key)

    scrambled_blocks = [blocks[i] for i in permutation]

    with open(output_path, "wb") as f:
        f.write(struct.pack(">Q", original_size))

        for block in scrambled_blocks:
            f.write(block)

    print("Scrambled executable created")


def create_db():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS licenses (
        license_key TEXT PRIMARY KEY,
        exe_hash TEXT NOT NULL,
        activation_key TEXT NOT NULL,
        fingerprint_hash TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS activation_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_key TEXT,
        fingerprint_hash TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    print("Database tables created")


# -----------------------------
# DATABASE INSERT
# -----------------------------
def insert_license(license_key, exe_hash, activation_key):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO licenses
        (license_key, exe_hash, activation_key, fingerprint_hash)
        VALUES (?, ?, ?, NULL)
        """,
        (license_key, exe_hash, activation_key),
    )

    conn.commit()
    conn.close()


# -----------------------------
# MAIN PACKAGING PIPELINE
# -----------------------------
def package_executable(input_exe, output_folder):

    license_key = generate_key()
    activation_key = generate_key()

    scrambled_name = f"scrambled_{license_key}.exe"
    scrambled_path = os.path.join(output_folder, scrambled_name)

    scramble(input_exe, scrambled_path, activation_key)

    exe_hash = hash_file(scrambled_path)
    create_db()
    insert_license(license_key, exe_hash, activation_key)

    print("\nPackage created successfully")
    print("License Key:", license_key)
    print("Activation Key:", activation_key)
    print("Executable Hash:", exe_hash)
    print("Scrambled File:", scrambled_path)


if __name__ == "__main__":
    input_exe = filedialog.askopenfilename(
        title="Select your file",
        filetypes=[("All files", "*.*")],
    )
    output_folder = "build"

    os.makedirs(output_folder, exist_ok=True)

    package_executable(input_exe, output_folder)
