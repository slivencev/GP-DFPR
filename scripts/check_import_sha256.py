#!/usr/bin/env python3
"""Verify all imported stage-file bytes against the author-supplied SHA-256 index."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "IMPORT_SHA256.json").read_text(encoding="utf-8"))
if len(manifest) != 50:
    raise SystemExit(f"Unexpected manifest length: {len(manifest)} (expected 50)")
failures = []
for relative, expected in sorted(manifest.items()):
    target = root / relative
    if not relative.startswith("stages/") or not target.is_file():
        failures.append(f"Missing or unexpected stage path: {relative}")
        continue
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != expected:
        failures.append(f"Hash mismatch: {relative} ({actual} != {expected})")
if failures:
    raise SystemExit("\n".join(failures))
print(f"PASS: all {len(manifest)} imported source-package files match original SHA-256.")
