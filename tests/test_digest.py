import hashlib

from nain_mcp_validator.domain.digest import verify_sha256


def test_verify_sha256_matches_exact_digest() -> None:
    content = "deterministic-cad-specification-v1"
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()

    result = verify_sha256(content, digest)
    assert result.is_valid is True
    assert result.computed_digest == digest
    assert result.payload_byte_size == len(content.encode("utf-8"))


def test_verify_sha256_detects_mismatch() -> None:
    content = "actual-content"
    tampered_digest = "0000000000000000000000000000000000000000000000000000000000000000"

    result = verify_sha256(content, tampered_digest)
    assert result.is_valid is False
    assert result.expected_digest == tampered_digest
