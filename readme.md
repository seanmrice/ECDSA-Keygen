# ECDSA Key Generator - [ecdsa_keygen.py](ecdsa_keygen.py)

This Python script generates Elliptic Curve Digital Signature Algorithm (ECDSA) key pairs. It supports generating keys of varying strengths and provides multiple options for output.

Author: Sean Rice, ecdsagen@programmerscache.com

Current Version: 0.1.1

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
- Requires Python 3.6 or higher.
- Requires the [cryptography](https://pypi.org/project/cryptography/) package to use SECP256R1, SECP384R1, and SECP521R1 elliptic curves for key generation.

## Usage

Run the script from the command line with the following arguments:

```
python ecdsa_keygen.py [OPTIONS]
```

## Options

- `--processes`: Number of processes to use (default is the number of CPU cores).
- `--cpu`: Use CPU for key generation (default option).
- <span style="color: red;">PLANNED</span>  `--cuda`: Use CUDA for key generation.
- <span style="color: red;">PLANNED</span> `--opencl`: Use OpenCL for key generation.
- `--file-out`: Specify the output file name for the keys.
- `--encrypt`: Provide an encryption passcode for the key files.
- `--out-count`: Set the number of key pairs to generate (default is 1).
- `--strength`: Select the strength level (0: SECP256R1, 1: SECP384R1, 2: SECP521R1).
- `--json`: Output keys in JSON format.
- `--continuous`: Continuously generate key pairs until the script is stopped unless paired with `--out-count`.

## Global Options
`OUTPUT_FOLDER`: - The folder where the key files will be saved. Defaults to the `output` directory.

`CONSOLE_KEYPAIR_DELIMITER` - The delimiter used to separate the private and public keys when outputting to the console. Defaults to:

`
"----------------------------------------------------------------"
`

(The standard width of the keypairs in the console).

`DISPLAY_CONSOLE_DELIMITER` - Whether or not to display the delimiter when outputting to the console. Defaults to `True`.

`TRACK_TIMING` - Whether or not to track the average key generation time. Defaults to `True`.

## Examples

Generate a single key pair using SECP256R1 and output to the console:

```
python ecdsa_keygen.py
```
Example Output:

```
-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgH4BjBCP01ZaWnYhj
j2fzzOZoOqupoBfopyVwI1B9YNahRANCAARabKrrXm1Y5DeEKJOkdRxcBHTaEBAE
LpbAJH++cWSfEe5YP98z/2TMJ1NYRJlkXPll7y1acoNi9WNNmpiSOquY
-----END PRIVATE KEY-----

-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEWmyq615tWOQ3hCiTpHUcXAR02hAQ
BC6WwCR/vnFknxHuWD/fM/9kzCdTWESZZFz5Ze8tWnKDYvVjTZqYkjqrmA==
-----END PUBLIC KEY-----
```
*Note, a delimiter will not be displayed when only a single key pair is generated, or when `DISPLAY_CONSOLE_DELIMITER` is set to `False`.*

Generate 5 key pairs using SECP384R1 and save to files with encryption:

```
python ecdsa_keygen.py --strength 1 --out-count 5 --file-out mykey --encrypt mypassword
```
Generate 10 key pairs using SECP521R1 and output in JSON format:

```
python ecdsa_keygen.py --strength 2 --out-count 10 --json
```
Example output: [keys.json](output/keys.json)

`--file-out` and `--json` can be used together to save the keys to files and output the keys in JSON format with a custom filename.
```
python ecdsa_keygen.py --strength 2 --out-count 10 --file-out keytest --json
```
Example output: [keytest.json](output/keytest.json)


## Output

- Keys are output to the console by default.
- When `--file-out` is used, keys are saved to separate `.pem` files in the `output` directory.
- If `--json` is selected, a JSON file containing the keys is created in the `output` directory.

<br>
<br>
<br >

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


## License

These scripts are released under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/) - [License File](LICENSE).

## Why?
To answer simply, why not?

While I understand it's essentially reinventing the wheel, I wanted to create a simple script that would allow me to generate ECDSA key pairs for use in my own projects; as well as to learn more about the ECDSA algorithm and how it works.  This is a nice standard way to generate bulk ECDSA key pairs, that can be delivered in a variety of manners.

Enjoy responsibly :)