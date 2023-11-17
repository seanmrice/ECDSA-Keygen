# v 0.1.0
Initial commit
- Generation of ECDSA key pairs.
- Supports multiple elliptic curves: SECP256R1, SECP384R1, and SECP521R1.
- Ability to use multiprocessing for faster key generation.
- Options for outputting keys in JSON format or saving to files.
- Tracking of average key generation time.
- Optional password encryption for key files.
- CPU support
- Deserialization of keys from JSON

# v 0.1.1
- Fix password encryption
- Continuous key generation
- Fix key generation time tracking
- Parallel key generation