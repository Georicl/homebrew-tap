#!/usr/bin/env python3
"""Update the tap from the published latest seqviz-rs release. Uses stdlib and gh."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

UPSTREAM = "Georicl/seqviz-rs"
TARGETS = (
    "aarch64-apple-darwin",
    "x86_64-apple-darwin",
    "x86_64-unknown-linux-musl",
)
ARCHIVES = tuple(f"seqviz-rs-{target}.tar.gz" for target in TARGETS)
FORMULA = Path(__file__).resolve().parents[2] / "Formula/seqviz-rs.rb"


def gh(*arguments: str) -> str:
    return subprocess.check_output(["gh", *arguments], text=True)


def parse_checksums(text: str) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-fA-F]{64}) [ *](\S+)", line)
        if match is None:
            raise ValueError(f"Invalid SHA256SUMS line: {line!r}")
        digest, name = match.groups()
        if name in checksums:
            raise ValueError(f"Duplicate checksum for {name}")
        checksums[name] = digest.lower()
    if set(checksums) != set(ARCHIVES):
        raise ValueError("SHA256SUMS must contain exactly the three supported archives")
    return checksums


def validate_assets(release: dict, tag: str) -> None:
    required = {*ARCHIVES, "SHA256SUMS"}
    assets = [asset for asset in release["assets"] if asset["name"] in required]
    names = [asset["name"] for asset in assets]
    if len(names) != len(required) or set(names) != required:
        raise ValueError("Release must contain the three supported archives and SHA256SUMS")
    for asset in assets:
        expected = f"https://github.com/{UPSTREAM}/releases/download/{tag}/{asset['name']}"
        if asset.get("browser_download_url") != expected:
            raise ValueError(f"Unexpected asset URL: {asset['name']}")
        if asset.get("state") != "uploaded" or asset.get("size", 0) <= 0:
            raise ValueError(f"Release asset is not ready: {asset['name']}")


def render_formula(tag: str, sums: dict[str, str]) -> str:
    if re.fullmatch(r"v\d+\.\d+\.\d+", tag) is None:
        raise ValueError("Expected a stable tag such as v0.1.0")
    version = tag[1:]
    base = f"https://github.com/{UPSTREAM}/releases/download/{tag}"
    arm, intel, linux = ARCHIVES
    return f'''class SeqvizRs < Formula
  desc "Terminal browser for biological sequences and alignment records"
  homepage "https://github.com/Georicl/seqviz-rs"
  version "{version}"
  license "MIT"

  on_macos do
    on_arm do
      url "{base}/{arm}"
      sha256 "{sums[arm]}"
    end

    on_intel do
      url "{base}/{intel}"
      sha256 "{sums[intel]}"
    end
  end

  on_linux do
    depends_on arch: :x86_64

    url "{base}/{linux}"
    sha256 "{sums[linux]}"
  end

  conflicts_with "sq", because: "both install an sq executable"

  def install
    bin.install "sq"
    pkgshare.install "config", "contrib"
  end

  test do
    ENV["XDG_CACHE_HOME"] = (testpath/"cache").to_s
    (testpath/"example.fa").write ">record1 example\\nACGT\\nTGCA\\n>record2\\nNNNN\\n"
    assert_equal ">record1 example\\nACGTTGCA\\n>record2\\nNNNN\\n",
                 shell_output("#{{bin}}/sq #{{testpath}}/example.fa")
    assert_equal "sq #{{version}}\\n", shell_output("#{{bin}}/sq --version")
  end
end
'''


def update(tag: str) -> bool:
    if re.fullmatch(r"v\d+\.\d+\.\d+", tag) is None:
        raise ValueError("Expected a stable tag such as v0.1.0")
    release = json.loads(gh("api", f"repos/{UPSTREAM}/releases/latest"))
    latest = release["tag_name"]
    if tag != latest:
        print(f"No change: {tag} is not the published latest release ({latest})")
        return False
    if release["draft"] or release["prerelease"]:
        raise ValueError("Latest release must be published and stable")
    validate_assets(release, tag)
    text = gh("release", "download", tag, "--repo", UPSTREAM,
              "--pattern", "SHA256SUMS", "--output", "-")
    formula = render_formula(tag, parse_checksums(text))
    if FORMULA.exists() and FORMULA.read_text() == formula:
        print(f"No change: formula already matches {tag}")
        return False
    FORMULA.parent.mkdir(parents=True, exist_ok=True)
    FORMULA.write_text(formula)
    print(f"Updated Formula/seqviz-rs.rb to {tag}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="Published upstream tag, e.g. v0.1.0")
    args = parser.parse_args()
    try:
        update(args.tag)
    except (KeyError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Cannot update formula: {error}\n")


if __name__ == "__main__":
    main()
