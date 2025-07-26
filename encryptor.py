import os
import json
import base64
from hashlib import sha256
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class AESFileEncryptor:
    def __init__(self, password):
        self.key = sha256(password.encode()).digest()  # Derive AES-256 key

    def encrypt_file(self, file_path):
        iv = os.urandom(12)  # GCM standard nonce size
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(file_path, 'rb') as f:
            plaintext = f.read()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        tag = encryptor.tag

        out_path = file_path + '.enc'
        with open(out_path, 'wb') as f:
            f.write(iv + tag + ciphertext)

        metadata = {
            "original_name": os.path.basename(file_path),
            "encrypted_name": os.path.basename(out_path),
            "timestamp": datetime.now().isoformat(),
            "sha256": sha256(plaintext).hexdigest()
        }

        self._store_metadata(metadata)
        return out_path

    def decrypt_file(self, enc_path, output_path):
        with open(enc_path, 'rb') as f:
            iv = f.read(12)
            tag = f.read(16)
            ciphertext = f.read()

        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        with open(output_path, 'wb') as f:
            f.write(plaintext)

        # Check hash
        if self._verify_hash(enc_path, sha256(plaintext).hexdigest()):
            print("[+] File integrity verified.")
        else:
            print("[!] WARNING: File integrity check failed.")

        return plaintext

    def _store_metadata(self, entry):
        if not os.path.exists("metadata_store.json"):
            with open("metadata_store.json", 'w') as f:
                json.dump([], f)

        with open("metadata_store.json", 'r+') as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=4)

    def _verify_hash(self, encrypted_filename, current_hash):
        try:
            with open("metadata_store.json", 'r') as f:
                records = json.load(f)
                for entry in records:
                    if entry['encrypted_name'] in encrypted_filename:
                        return entry['sha256'] == current_hash
        except:
            return False
        return False
