from encryptor import AESFileEncryptor
import os

def print_menu():
    print("\n🔐 Secure File Storage System")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. Exit")

def main():
    password = input("Enter master password: ")
    engine = AESFileEncryptor(password)

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            path = input("Enter full path of file to encrypt: ").strip()
            if os.path.isfile(path):
                out_file = engine.encrypt_file(path)
                print(f"[+] File encrypted and saved as: {out_file}")
            else:
                print("[!] Invalid file path.")
        
        elif choice == '2':
            path = input("Enter full path of .enc file: ").strip()
            if os.path.isfile(path):
                out_file = input("Enter name to save decrypted file as: ").strip()
                try:
                    engine.decrypt_file(path, out_file)
                    print(f"[+] Decrypted file saved as: {out_file}")
                except Exception as e:
                    print(f"[!] Decryption failed: {e}")
            else:
                print("[!] Invalid encrypted file path.")

        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("[!] Invalid choice.")

if __name__ == "__main__":
    main()
