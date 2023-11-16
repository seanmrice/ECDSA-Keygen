import argparse
import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

INPUT_FOLDER = "output"
OUTPUT_FOLDER = "keys_output"

def generate_fernet_key(password, salt):
    # Generates a Fernet key based on the given password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def decrypt_data(encrypted_data, password):
    salt = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]

    key = generate_fernet_key(password, salt)
    fernet = Fernet(key)

    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data).decode()

    return decrypted_data


def load_json_keys(filename, password=None):
    filename = os.path.join(INPUT_FOLDER, filename)
    with open(filename, 'rb') as file:
        data = file.read()
        if password is None:
            return json.loads(data)
        else: # Decrypt the data
            decrypted_data = decrypt_data(data, password)
            try:
                return json.loads(decrypted_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Decryption successful but data is not valid JSON. {e}") from e

def add_pem_headers(key_str, is_private):
    if is_private:
        return "-----BEGIN PRIVATE KEY-----\n" + key_str + "\n-----END PRIVATE KEY-----"
    else:
        return "-----BEGIN PUBLIC KEY-----\n" + key_str + "\n-----END PUBLIC KEY-----"

def save_key_to_file(key_str, filename, out_dir='.'):
    # Create output directory if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    filename = os.path.join(out_dir, filename)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(key_str)

def main():
    parser = argparse.ArgumentParser(description='PEM Key Pair Generator from JSON')
    parser.add_argument('--json-file', type=str, required=True, help='JSON file containing key pairs')
    parser.add_argument('--decrypt', type=str, help='Encryption key, if the private keys are encrypted')
    parser.add_argument('--out-dir', type=str, default='output', help='Output directory')
    args = parser.parse_args()
    
    if args.decrypt:
        key_pairs = load_json_keys(args.json_file, password=args.decrypt)
    else:
        key_pairs = load_json_keys(args.json_file)
    
    OUTPUT_FOLDER = args.out_dir
    if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
        
    for i, (priv_key, pub_key) in enumerate(key_pairs.items(), start=1):
        priv_pem = add_pem_headers(priv_key, is_private=True)
        pub_pem = add_pem_headers(pub_key, is_private=False)
        save_key_to_file(priv_pem, f"{i}-priv.pem", out_dir=OUTPUT_FOLDER)
        save_key_to_file(pub_pem, f"{i}-pub.pem", out_dir=OUTPUT_FOLDER)

if __name__ == "__main__":
    main()
