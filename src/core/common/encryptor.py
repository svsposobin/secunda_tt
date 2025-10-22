from hashlib import sha256 as hashlib_sha256


class EncryptorProcessor:
    """Упрощенный "энкриптор", в реальной сфере использовать salt, cryptography и хеширования по secret key"""

    @staticmethod
    def encrypt(data: str) -> bytes:
        return hashlib_sha256(data.encode()).digest()

    @staticmethod
    def is_equal(data: str, hashed_data: bytes) -> bool:
        return hashlib_sha256(data.encode()).digest() == hashed_data
