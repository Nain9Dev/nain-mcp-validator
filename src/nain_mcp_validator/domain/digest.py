import hashlib

from pydantic import BaseModel


class DigestVerificationResult(BaseModel):
    is_valid: bool
    computed_digest: str
    expected_digest: str
    payload_byte_size: int

def verify_sha256(data: bytes | str, expected_sha256: str) -> DigestVerificationResult:
    if isinstance(data, str):
        payload_bytes = data.encode("utf-8")
    else:
        payload_bytes = data

    computed = hashlib.sha256(payload_bytes).hexdigest()
    is_valid = computed.lower() == expected_sha256.lower().strip()

    return DigestVerificationResult(
        is_valid=is_valid,
        computed_digest=computed,
        expected_digest=expected_sha256.strip(),
        payload_byte_size=len(payload_bytes),
    )
