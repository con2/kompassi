import json
from collections.abc import Sequence
from typing import Self

from cryptography.hazmat.primitives.keywrap import InvalidUnwrap
from django.contrib.auth.models import User
from django.db import models
from jwskate import JweCompact, Jwk

from kompassi.event_log_v2.utils.monthly_partitions import UUID7Mixin, uuid7

# https://guillp.github.io/jwskate/#supported-encryption-algorithms
EC_ALG = "ECDH-ES+A256KW"
EC_CURVE = "P-256"
SYM_ALG = "A256GCM"
PBE_ALG = "PBES2-HS512+A256KW"


class WrongPassword(ValueError):
    pass


class WrongKey(ValueError):
    pass


class KeyPair(UUID7Mixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="keypairs")
    public_key = models.JSONField()
    encrypted_private_key = models.TextField()

    @classmethod
    def generate_for_user(cls, user: User, password: str, check_password: bool = True):
        """
        Generates an asymmetric crypto keypair for the user. The public key is
        stored unencrypted in the database, and the private key is encrypted
        with the user's password.
        """
        if check_password and not user.check_password(password):
            raise WrongPassword()

        kid = uuid7()
        private_key = Jwk.generate(alg=EC_ALG, crv=EC_CURVE, kid=str(kid))
        public_key = private_key.public_jwk()

        encrypted_private_key = JweCompact.encrypt_with_password(
            json.dumps(dict(private_key)).encode(),
            password=password,
            alg=PBE_ALG,
            enc=SYM_ALG,
        )

        return cls.objects.create(
            id=kid,
            user=user,
            public_key=dict(public_key),
            encrypted_private_key=str(encrypted_private_key),
        )

    @classmethod
    def get_for_user(cls, user: User):
        return cls.objects.filter(user=User).latest("id")

    def reencrypt_private_key(
        self,
        old_password: str,
        new_password: str,
    ):
        """
        Re-encrypts the private key with a new password.
        Must be called when changing the user's password.
        """
        private_key_bytes = JweCompact(self.encrypted_private_key).decrypt_with_password(old_password)

        encrypted_private_key = JweCompact.encrypt_with_password(
            private_key_bytes,
            password=new_password,
            alg=PBE_ALG,
            enc=SYM_ALG,
        )

        self.encrypted_private_key = str(encrypted_private_key)
        self.save(update_fields=["encrypted_private_key"])

    def get_decrypted_private_key(self, password: str):
        try:
            return json.loads(JweCompact(self.encrypted_private_key).decrypt_with_password(password))
        except InvalidUnwrap as e:
            raise WrongPassword() from e

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypts the plaintext using the public key of the keypair.
        """
        return str(
            JweCompact.encrypt(
                plaintext.encode(),
                key=self.public_key,
                alg=EC_ALG,
                enc=SYM_ALG,
            )
        )

    def decrypt(self, ciphertext: str, password: str) -> str:
        """
        Tries to decrypt the ciphertext using the private key of the keypair.
        """
        private_key = self.get_decrypted_private_key(password)

        try:
            return JweCompact(ciphertext).decrypt(key=private_key, alg=EC_ALG).decode()
        except InvalidUnwrap as e:
            raise WrongKey() from e

    @classmethod
    def encrypt_multi(cls, plaintext: str, recipients: Sequence[Self]) -> dict[str, str]:
        """
        Encrypts the plaintext using multiple public keys.
        """
        return {
            str(keypair.id): str(
                JweCompact.encrypt(
                    plaintext.encode(),
                    key=keypair.public_key,
                    alg=EC_ALG,
                    enc=SYM_ALG,
                )
            )
            for keypair in recipients
        }

    def decrypt_multi(self, ciphertexts: dict[str, str], password: str) -> str:
        """
        Tries to decrypt the ciphertext using the private key of the keypair.
        """
        kid = str(self.id)
        ciphertext = ciphertexts.get(kid)

        if ciphertext is None:
            raise WrongKey()

        return self.decrypt(ciphertext, password)
