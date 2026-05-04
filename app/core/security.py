import hashlib


def pseudonymize_user(user_identifier: str, structural_salt: str) -> str:
    return hashlib.sha256(f"{user_identifier}{structural_salt}".encode()).hexdigest()
