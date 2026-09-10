#!/usr/bin/env python3
"""Package only public website files for deployment."""
import hashlib
from pathlib import Path
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
PAGES = [f"{language}{page}index.html" for language in ("", "en/")
         for page in ("", "privacy/", "terms/", "support/")]
ASSETS = ["assets/logo.png", "assets/home.css", "assets/document.css", "assets/shared.css"]
ASSETS += [f"assets/screenshots/{name}.png" for name in (
    "03c-plan-12week", "04-coach-chat", "05-library", "07-active-workout", "08-me-subscribed")]

def main():
    output = Path(sys.argv[1]).resolve()
    files = sorted(PAGES + ASSETS)
    for name in files:
        path = ROOT / name
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            raise SystemExit(f"Invalid public file: {name}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output, "w:gz") as archive:
        for name in files:
            archive.add(ROOT / name, arcname=name, recursive=False)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n")
    print(f"Packaged {len(files)} public files: {output.name} ({digest})")

if __name__ == "__main__":
    main()
