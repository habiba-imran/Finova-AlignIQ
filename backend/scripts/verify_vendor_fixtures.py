"""Read-only offline verification. Prints counts/static codes, never captured text or paths."""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.semantics.fixtures import FixtureVerificationError, load_manifest, verify_fixture  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).resolve().parents[1] / "vendor_verification/manifest.json")
    parser.add_argument("--fixture-root", type=Path, help="Authorized local read-only capture root; no files are copied")
    args = parser.parse_args()
    try:
        manifest = load_manifest(args.manifest)
        records = [record for record in manifest.fixtures if record.status == "REVIEWED"]
        if not records:
            print("NO_AUTHENTIC_ORACLES: 0 reviewed captures; vendor normalization disabled.")
            return 2
        if args.fixture_root is None:
            print("FIXTURE_ROOT_REQUIRED")
            return 1
        for record in records:
            verify_fixture(record, args.fixture_root)
        print(f"ORACLE_CHECKS_PASSED: {len(records)}; this does not approve or enable vendor mappings.")
        return 0
    except FixtureVerificationError as error:
        print(str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
