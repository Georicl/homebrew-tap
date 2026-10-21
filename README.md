# Homebrew tap for seqviz-rs

Install the prebuilt terminal sequence browser from the public [seqviz-rs releases](https://github.com/Georicl/seqviz-rs/releases):

```sh
brew install Georicl/tap/seqviz-rs
sq --version
sq genome.fa
```

The package is named `seqviz-rs`; its executable is `sq`. Homebrew's unrelated `sq` formula installs the same executable, so the two formulae conflict.

Supported downloads: Apple Silicon macOS, Intel macOS and x86_64 Linux. Rust is not required. Example application and yazi configuration files are installed under `$(brew --prefix seqviz-rs)/share/seqviz-rs/`; installation does not change your own configuration.

Update an installed version:

```sh
brew update
brew upgrade Georicl/tap/seqviz-rs
```

Each formula version pins the upstream release URL and the SHA-256 for each architecture. The upstream release workflow updates this tap after publishing a new latest release. Historical releases and identical reruns leave the formula unchanged.

Maintainers can generate the same formula manually, with Python 3 and GitHub CLI installed:

```sh
python3 .github/scripts/update-formula.py --tag v0.1.0
```

The script reads public upstream release metadata and `SHA256SUMS`; it writes only `Formula/seqviz-rs.rb`. Commit and push the resulting change after review. Tap CI installs and tests the actual prebuilt package on all three supported platforms.

This tap and seqviz-rs are licensed under MIT.
