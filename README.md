# 🔐 Secure File Storage System – FileLocker

**FileLocker** is a Python-based CLI tool that lets users securely **encrypt and decrypt files** using **AES-256 GCM** encryption. It uses a password-derived key, verifies file integrity using SHA-256, and tracks encryption history in a local metadata file.

---

## How It Works

1. **User enters a master password**
   - This password is used to derive a secure AES-256 key using SHA-256 hashing.
   
2. **Encrypting a file**
   - AES-GCM mode is used to encrypt the file securely.
   - An `.enc` file is generated, and a metadata entry is logged with timestamp and SHA-256 hash of the original file.

3. **Decrypting a file**
   - User selects an encrypted file and provides a name for the decrypted output.
   - File is decrypted using the same password-derived key.
   - The system verifies the integrity of the decrypted file by comparing its hash with the original hash stored in metadata.

4. **File integrity check**
   - If the SHA-256 hash matches the stored value, a success message is shown.
   - Otherwise, a warning is displayed.

---

## Requirements

- Python 3.6+
- `cryptography` library

Install the required library:

```bash
pip install cryptography

