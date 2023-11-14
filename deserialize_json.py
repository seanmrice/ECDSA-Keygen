import argparse
import json
import os

def load_json_keys(filename):
    with open(filename, 'r') as file:
        return json.load(file)

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
    with open(filename, 'w') as file:
        file.write(key_str)

def main():
    parser = argparse.ArgumentParser(description='PEM Key Pair Generator from JSON')
    parser.add_argument('--json-file', type=str, required=True, help='JSON file containing key pairs')
    parser.add_argument('--encrypt-key', type=str, help='Encryption key, if the private keys are encrypted')
    parser.add_argument('--out-dir', type=str, default='.', help='Output directory')
    args = parser.parse_args()

    key_pairs = load_json_keys(args.json_file)
    for i, (priv_key, pub_key) in enumerate(key_pairs.items(), start=1):
        priv_pem = add_pem_headers(priv_key, is_private=True)
        pub_pem = add_pem_headers(pub_key, is_private=False)

        save_key_to_file(priv_pem, f"{i}-priv.pem", out_dir=args.out_dir)
        save_key_to_file(pub_pem, f"{i}-pub.pem", out_dir=args.out_dir)

if __name__ == "__main__":
    main()
