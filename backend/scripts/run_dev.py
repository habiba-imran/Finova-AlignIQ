"""Loopback development runner; explicitly load an optional private settings file."""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.development_env import load_development_env  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path)
    args = parser.parse_args()
    if args.env_file:
        try:
            load_development_env(args.env_file)
        except ValueError:
            print("DEVELOPMENT_ENV_UNAVAILABLE_OR_INVALID")
            return 1
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, access_log=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
