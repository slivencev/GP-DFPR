#!/usr/bin/env python3
"""Import ONLY author-selected source-package entries from a checksum-pinned Zenodo deposit.

This importer never runs downloaded research code. It refuses an unexpected public
archive or any pre-existing GitHub file with bytes different from the original.
Run from the repository root; intended for a one-off GitHub Actions job.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.request
import zipfile

RECORD_ID = 22893667
ARCHIVE_NAME = "Supplementary_Data_S2.zip"
EXPECTED_SHA256 = "846419b0187d70a04d7572debbcecd58015f15369e3b1683b7efa8e4bec25682"

# Hashes were read from the author's uploaded Supplementary Data S2.
STAGE_SHA256 = {
    "GP_DFPR_Partial_Observation_v3": "a7632b62beda8f2a791b72b1257855aeb7ee146425e5dc578c782f1b568d646a",
    "GP_DFPR_Periodic_v9": "e4965a1a1615b341d94a1b4267024d618d51f506e2c931c1a4ae41a1c76af339",
    "GP_DFPR_Scheduling_v11": "05695073a2fb33df3b2f1c8d48aa934a4d79436f87c8d93a98ae18c7bd440ac0",
    "GP_DFPR_Matched_Schedules_v12": "6728cf52edae3e7dd13c72945a7d32a82ae88a1596f6a91aceb6d4f6b08c6256",
    "GP_DFPR_Positioning_v13": "24bd255e5e4ae393961cb0256bc66d74a62160c7e8375f21615a5a239159d214",
    "GP_DFPR_Observation_Model_v14": "4c84382f60fe60e62a1e384e0f2459d5ac3536e99134fd6188d92865126d5fe8",
    "GP_DFPR_MCS_Observation_v15": "a0cf5fab8b95acd285f383838a3f226c3b29254e405ae6647311d8cec41fa997",
    "GP_DFPR_Research_Objective_v16": "acedc184dc1a499e6228a00781aeb6bd9affba36e7e7b0c06473a9919bc99a30",
}

# Exact file selection from the author's GP_DFPR_GitHub_Source_Import.zip.
SELECTED = {
    "GP_DFPR_Partial_Observation_v3": [
        "PROTOCOL.md", "REPORT_RU.md", "TESTS.txt", "THEORY.md",
        "make_report.py", "prototype.py", "requirements.txt", "test_prototype.py",
    ],
    "GP_DFPR_Periodic_v9": [
        "CERTIFICATE_BOUND.md", "PROTOCOL.md", "REPORT_RU.md", "TESTS.txt",
        "model.py", "periodic.py", "requirements.txt", "run_study.py",
    ],
    "GP_DFPR_Scheduling_v11": [
        "PROTOCOL.md", "REPORT_RU.md", "RESEARCH_CHECKPOINT.md", "TESTS.json",
        "THEORY.md", "examples.json", "requirements.txt", "run_audit.py", "scheduler.py",
    ],
    "GP_DFPR_Matched_Schedules_v12": [
        "INTERPRETATION.md", "PROTOCOL.md", "REPORT_RU.md", "RESEARCH_CHECKPOINT.md",
        "contexts.json", "model.py", "requirements.txt", "run_compare.py", "scheduler.py",
    ],
    "GP_DFPR_Observation_Model_v14": [
        "EXISTING_EXTERNAL_CALIBRATION.json", "OBSERVATION_MODEL_RU.md",
        "README.md", "TESTS.txt", "evidence.py", "package.py", "test_evidence.py",
    ],
    "GP_DFPR_MCS_Observation_v15": [
        "PROTOCOL.md", "REPORT_RU.md", "RESEARCH_CHECKPOINT.md", "SOURCE_LICENSE",
        "UPSTREAM_PROVENANCE.md", "curves.json", "observation.py",
        "requirements.txt", "run_study.py",
    ],
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def download_verified_archive():
    api_url = f"https://zenodo.org/api/records/{RECORD_ID}"
    with urllib.request.urlopen(
        urllib.request.Request(api_url, headers={"User-Agent": "GP-DFPR archival verification"}),
        timeout=45,
    ) as response:
        record = json.load(response)
    if str(record.get("id")) != str(RECORD_ID):
        raise RuntimeError("Wrong Zenodo record ID")
    matches = [f for f in record.get("files", []) if f.get("key") == ARCHIVE_NAME]
    if len(matches) != 1:
        raise RuntimeError(
            f"Published record does not expose exactly one {ARCHIVE_NAME}; "
            "do not substitute a different deposit or unpublished file."
        )
    links = matches[0].get("links", {})
    url = links.get("self") or links.get("content")
    if not url or not url.startswith("https://"):
        raise RuntimeError("No secure download link for the exact published file")
    print("Downloading DOI-record file:", ARCHIVE_NAME)
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "GP-DFPR archival verification"}),
        timeout=180,
    ) as response:
        data = response.read(100_000_000)
    if sha256(data) != EXPECTED_SHA256:
        raise RuntimeError(
            f"Public archive SHA-256 {sha256(data)} differs from author's uploaded "
            f"SHA-256 {EXPECTED_SHA256}. Nothing will be imported."
        )
    print("Public archive is byte-identical to author's uploaded Supplementary Data S2.")
    return data


def main():
    if not Path("README.md").is_file() or not Path("docs/REPRODUCIBILITY.md").is_file():
        raise RuntimeError("Run from GP-DFPR repository root")
    data = download_verified_archive()
    staged = {}
    manifest = {}
    with zipfile.ZipFile(io.BytesIO(data)) as outer:
        if outer.testzip() is not None:
            raise RuntimeError("Damaged outer archive")
        archived_hashes = json.loads(outer.read("SOURCE_ARCHIVES.json"))
        if archived_hashes != {name + ".zip": digest for name, digest in STAGE_SHA256.items()}:
            raise RuntimeError("Source archive list/hash mismatch")
        for stage, expected_hash in STAGE_SHA256.items():
            nested_name = f"evidence_archives/{stage}.zip"
            payload = outer.read(nested_name)
            if sha256(payload) != expected_hash:
                raise RuntimeError(f"Invalid nested digest: {nested_name}")
            if stage not in SELECTED:
                continue
            with zipfile.ZipFile(io.BytesIO(payload)) as z:
                if z.testzip() is not None:
                    raise RuntimeError(f"Damaged nested archive: {stage}")
                for name in SELECTED[stage]:
                    original = z.read(f"{stage}/{name}")
                    dest = Path("stages") / stage / name
                    if dest.is_file() and dest.read_bytes() != original:
                        raise RuntimeError(
                            f"Existing GitHub file has different bytes: {dest}. "
                            "Do not silently overwrite prior commits."
                        )
                    staged[dest] = original
                    manifest[str(dest).replace(os.sep, "/")] = sha256(original)
    # All checks must succeed before the first source file is written.
    for path, original in staged.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(original)
    Path("IMPORT_SHA256.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Imported and SHA-256 indexed {len(staged)} original stage files.")
    if len(staged) != 50:
        raise RuntimeError(f"Unexpected number of selected files: {len(staged)}")
    print("Existing documentation and independently archived bulk experiment data unchanged.")
    print("This import does not rerun simulations or solve the missing v8 predecessor.")


if __name__ == "__main__":
    main()
