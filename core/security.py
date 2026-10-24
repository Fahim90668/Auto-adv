import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from core.config import settings

def get_aes_key() -> bytes:
    # Expects a 32-byte key encoded in hex or base64, or raw bytes
        key_input = settings.ENCRYPTION_KEY
            try:
                    return base64.b64decode(key_input)
                        except Exception:
                                return bytes.fromhex(key_input)

                                def encrypt_token(token: str) -> tuple[str, str]:
                                    key = get_aes_key()
                                        aesgcm = AESGCM(key)
                                            nonce = os.urandom(12)  # 12 bytes nonce for GCM
                                                ciphertext = aesgcm.encrypt(nonce, token.encode('utf-8'), None)
                                                    return (
                                                            base64.b64encode(ciphertext).decode('utf-8'),
                                                                    base64.b64encode(nonce).decode('utf-8')
                                                                        )

                                                                        def decrypt_token(ciphertext_b64: str, nonce_b64: str) -> str:
                                                                            key = get_aes_key()
                                                                                aesgcm = AESGCM(key)
                                                                                    ciphertext = base64.b64decode(ciphertext_b64)
                                                                                        nonce = base64.b64decode(nonce_b64)
                                                                                            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
                                                                                                return plaintext.decode('utf-8')