# ECDSA Key Generator - [ecdsa_keygen.py](ecdsa_keygen.py)

This Python script generates Elliptic Curve Digital Signature Algorithm (ECDSA) key pairs. It supports generating keys of varying strengths and provides multiple options for output.

Author: Sean Rice, ecdsagen@programmerscache.com

Current Version: 0.1.0

## Features

- Generation of ECDSA key pairs.
- Supports multiple elliptic curves: SECP256R1, SECP384R1, and SECP521R1.
- Ability to use multiprocessing for faster key generation.
- Options for outputting keys in JSON format or saving to files.
- Tracking of average key generation time.
- Optional password encryption for key files.

## Requirements

Before running the script, ensure you have the required packages installed:

```
pip install -r requirements.txt
```

## Usage

Run the script from the command line with the following arguments:

```
python ecdsa_keygen.py [OPTIONS]
```

### Options

- `--processes`: Number of processes to use (default is the number of CPU cores).
- `--cpu`: Use CPU for key generation (default option).
- `--cuda`: <span style="color: red;">PLANNED FEATURE</span> - Use CUDA for key generation.
- `--opencl`: <span style="color: red;">PLANNED FEATURE</span> - Use OpenCL for key generation.
- `--file-out`: Specify the output file name for the keys.
- `--encrypt`: Provide an encryption passcode for the key files.
- `--out-count`: Set the number of key pairs to generate (default is 1).
- `--strength`: Select the strength level (0: SECP256R1, 1: SECP384R1, 2: SECP521R1).
- `--json`: Output keys in JSON format.

### Examples

Generate a single key pair using SECP256R1 and output to the console:

```
python ecdsa_keygen.py
```


Generate 5 key pairs using SECP384R1 and save to files with encryption:

```
python ecdsa_keygen.py --strength 1 --out-count 5 --file-out mykey --encrypt mypassword
```
Generate 10 key pairs using SECP521R1 and output in JSON format:

```
python ecdsa_keygen.py --strength 2 --out-count 10 --json
```

## Output

- Keys are output to the console by default.
- When `--file-out` is used, keys are saved to separate `.pem` files in the `output` directory.
- If `--json` is selected, a JSON file containing the keys is created in the `output` directory.


# Deserialize JSON to PEM Key Pair Generator - [deserialize_json.py](deserialize_json.py)
This script, deserialize_json.py, is designed to take a JSON file containing ECDSA key pairs and generate PEM files for each key pair.

## Features

- Loads key pairs from a JSON file.
- Adds appropriate PEM headers to both private and public keys.
- Saves the keys as separate PEM files in a specified directory.

## Usage

Run the script from the command line with the following arguments:

```
python deserialize_json.py --json-file <path_to_json_file> [--encrypt-key <encryption_key>] [--out-dir <output_directory>]
```

## Arguments

- `--json-file`: The path to the JSON file containing the key pairs.
- `--encrypt-key`: (Optional) The encryption key, if the private keys in the JSON file are encrypted.
- `--out-dir`: (Optional) The output directory where the PEM files will be saved. Defaults to the current directory.

## Example

Convert keys from a JSON file and save the PEM files to a specific directory:

```
python deserialize_json.py --json-file keys.json --out-dir ./pem_keys
```

This will read the key pairs from keys.json and save the PEM files in the ./pem_keys directory.

## Output
- Private keys are saved with the filename format [index]-priv.pem.
- Public keys are saved with the filename format [index]-pub.pem.


# License

These scripts are released under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/) - [License File](LICENSE).
