#!/usr/bin/env python3
"""Download the exact OpenRichpedia source files used by this course project."""
from __future__ import annotations

import argparse
from pathlib import Path
from urllib.request import Request, urlopen

UPSTREAM_COMMIT = "0ded4b2c9414160b5b39914d43e42168e4d0762c"
BASE = f"https://raw.githubusercontent.com/OpenKG-ORG/OpenRichpedia/{UPSTREAM_COMMIT}"
FILES = {
    "city.js": "data_src/city_sight/city.js",
    "city_sight.js": "data_src/city_sight/city_sight.js",
    "pic_city.js": "data_src/city_sight/pic_city.js",
    "contain.js": "data_src/city_sight/contain.js",
    "people.js": "data_src/people/people.js",
    "pic_people.js": "data_src/people/pic_people.js",
}


def download(output_dir: Path, force: bool = False) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for local_name, upstream_path in FILES.items():
        target = output_dir / local_name
        if target.exists() and not force:
            print(f"[skip] {target}")
            continue
        url = f"{BASE}/{upstream_path}"
        print(f"[get ] {url}")
        request = Request(url, headers={"User-Agent": "openrichpedia-neo4j-course-project/1.0"})
        with urlopen(request, timeout=60) as response:
            target.write_bytes(response.read())
        print(f"[save] {target} ({target.stat().st_size:,} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/raw"))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    download(args.output, args.force)


if __name__ == "__main__":
    main()
