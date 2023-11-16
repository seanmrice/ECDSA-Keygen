import argparse
import os
import json
import time
from multiprocessing import Pool
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
import base64

#################################### Global Variables ##############################################
OUTPUT_FOLDER = "output"
CONSOLE_KEYPAIR_DELIMITER = "----------------------------------------------------------------"
DISPLAY_CONSOLE_DELIMITER = True
TRACK_TIMING = True
####################################################################################################

def generate_ecdsa_keys_sync(strength):
    if strength == 0:
        curve = ec.SECP256R1()
    elif strength == 1:
        curve = ec.SECP384R1()
    elif strength == 2:
        curve = ec.SECP521R1()
    else:
        raise ValueError("Invalid strength value. Choose 0, 1, or 2.")

    private_key = ec.generate_private_key(curve, default_backend())
    public_key = private_key.public_key()

    # Convert to PEM format
    private_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption()
    ).decode()
    
    public_pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    return private_pem, public_pem

def generate_fernet_key(password, salt):
    # Generates a Fernet key based on the given password and salt
    print(password)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_data(data, password):
    # Ensure data is a JSON string
    salt = os.urandom(16)
    key = generate_fernet_key(password, salt)
    fernet = Fernet(key)

    # Encrypt the data and return the salt and encrypted data
    return salt + fernet.encrypt(data.encode())


def save_keys_to_file_str(filename, private_pem, public_pem, password=None):
    print(password)
    filename = os.path.join(OUTPUT_FOLDER, filename)
    data_to_write = private_pem + public_pem

    if password is not None:
        data_to_write = encrypt_data(data_to_write, password)

    with open(filename, 'wb') as file:
        file.write(data_to_write)


def main():
    parser = argparse.ArgumentParser(description='ECDSA Key Generator')
    parser.add_argument('--processes', type=int, default=os.cpu_count(), help='Number of processes to use')
    parser.add_argument('--cpu', action='store_true', help='Use CPU for key generation')
    parser.add_argument('--cuda', action='store_true', help='Use CUDA for key generation')
    parser.add_argument('--opencl', action='store_true', help='Use OpenCL for key generation')
    parser.add_argument('--file-out', type=str, help='Output file name')
    parser.add_argument('--encrypt', type=str, help='Encryption passcode')
    parser.add_argument('--out-count', type=int, default=1, help='Number of key pairs to generate')
    parser.add_argument('--strength', type=int, default=0, choices=[0, 1, 2], help='Strength level (0: SECP256R1, 1: SECP384R1, 2: SECP521R1)')
    parser.add_argument('--json', action='store_true', help='Output keys in JSON format')
    args = parser.parse_args()

    if not (args.cuda or args.opencl):
        args.cpu = True
    # Estimate time for completion
    avg_time_per_key = get_average_time(str(args.strength))
    estimated_time = avg_time_per_key * args.out_count
    if avg_time_per_key > 0:
        keys_per_second = 1 / avg_time_per_key
        print(f"Average Keys/Second: {keys_per_second:.2f}")
    else:
        print("Average Keys/Second: Not available (no previous data)")

    print(f"Estimated time to completion: {estimated_time:.2f} seconds")
    
    # Timing the key generation
    if TRACK_TIMING:
        start_time = time.time()
    with Pool(processes=args.processes) as pool:
        key_pairs = pool.starmap(generate_ecdsa_keys_sync, [(args.strength,) for _ in range(args.out_count)])
    if TRACK_TIMING:
        end_time = time.time()
    keys = {}
    for i, (private_pem, public_pem) in enumerate(key_pairs):
        if args.json:
            # strip the header and footer from each key
            private_pem = private_pem.replace('-----BEGIN PRIVATE KEY-----\n', '').replace('-----END PRIVATE KEY-----\n', '').strip()
            public_pem = public_pem.replace('-----BEGIN PUBLIC KEY-----\n', '').replace('-----END PUBLIC KEY-----\n', '').strip()
            keys[private_pem] = public_pem
        elif args.file_out:
            filename = f"{args.file_out}-{i+1}.pem"
            # Call a modified save_keys_to_file function that expects strings
            print(args.encrypt)
            save_keys_to_file_str(filename, private_pem, public_pem, args.encrypt)
        else:
            print(private_pem)
            print(public_pem.replace('-----END PUBLIC KEY-----\n', '-----END PUBLIC KEY-----'))
            if DISPLAY_CONSOLE_DELIMITER and ( args.out_count > 1 ):
                print(CONSOLE_KEYPAIR_DELIMITER)

    if args.json:
        if args.file_out:
            json_filename = os.path.join(OUTPUT_FOLDER, f"{args.file_out}.json")
        else:
            json_filename = os.path.join(OUTPUT_FOLDER, "keys.json")
        
        if args.encrypt:
            encrypted_data = encrypt_data(json.dumps(keys), args.encrypt)
            with open(json_filename, 'wb') as json_file:
                json_file.write(encrypted_data)
                
        else:
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(keys, json_file, indent=4)

    # Update timing.json
    if TRACK_TIMING:
        total_time = end_time - start_time
        average_time = total_time / args.out_count
        update_timing_json(str(args.strength), average_time)
    
def update_timing_json(strength, new_time):
    timing_data = {}
    if os.path.exists('timing.json'):
        with open('timing.json', 'r', encoding='utf-8') as file:
            timing_data = json.load(file)

    if strength in timing_data:
        count, avg_time = timing_data[strength]
        new_avg = ((avg_time * count) + new_time) / (count + 1)
        timing_data[strength] = [count + 1, new_avg]
    else:
        timing_data[strength] = [1, new_time]

    with open('timing.json', 'w', encoding='utf-8') as file:
        json.dump(timing_data, file, indent=4)

    return timing_data[strength][1]

def get_average_time(strength):
    if os.path.exists('timing.json'):
        with open('timing.json', 'r', encoding='utf-8') as file:
            timing_data = json.load(file)
        return timing_data.get(str(strength), [0, 0])[1]
    return 0

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    main()
