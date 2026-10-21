"""Offline checks for the updater's release selection and checksum contract."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "update_formula", Path(__file__).with_name("update-formula.py")
)
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


def release(tag="v0.1.0"):
    return {
        "tag_name": tag,
        "draft": False,
        "prerelease": False,
        "assets": [
            {
                "name": name,
                "browser_download_url": f"https://github.com/{updater.UPSTREAM}/releases/download/{tag}/{name}",
                "state": "uploaded",
                "size": 100,
            }
            for name in (*updater.ARCHIVES, "SHA256SUMS")
        ],
    }


def checksum_text():
    return "".join(f"{'a' * 64}  {name}\n" for name in updater.ARCHIVES)


class UpdateFormulaTests(unittest.TestCase):
    def test_complete_checksums(self):
        self.assertEqual(set(updater.parse_checksums(checksum_text())), set(updater.ARCHIVES))

    def test_incomplete_duplicate_and_invalid_checksums(self):
        lines = checksum_text().splitlines(keepends=True)
        for text in ("".join(lines[:-1]), checksum_text() + lines[0], "bad  archive.tar.gz\n"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                updater.parse_checksums(text)

    def test_invalid_asset_set_and_url(self):
        metadata = release()
        metadata["assets"].pop()
        with self.assertRaises(ValueError):
            updater.validate_assets(metadata, "v0.1.0")
        metadata = release()
        metadata["assets"][0]["browser_download_url"] = "https://example.com/other.tar.gz"
        with self.assertRaises(ValueError):
            updater.validate_assets(metadata, "v0.1.0")

    def test_unrelated_release_assets_are_allowed(self):
        metadata = release()
        metadata["assets"].append({"name": "LICENSE"})
        updater.validate_assets(metadata, "v0.1.0")

    def test_older_tag_is_noop_without_download_or_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            formula = Path(tmp) / "formula.rb"
            formula.write_text("unchanged")
            with patch.object(updater, "FORMULA", formula), patch.object(
                updater, "gh", return_value=json.dumps(release("v0.2.0"))
            ) as gh:
                self.assertFalse(updater.update("v0.1.0"))
                gh.assert_called_once_with("api", "repos/Georicl/seqviz-rs/releases/latest")
            self.assertEqual(formula.read_text(), "unchanged")

    def test_latest_updates_and_identical_rerun_is_noop(self):
        def gh(*args):
            if args == ("api", "repos/Georicl/seqviz-rs/releases/latest"):
                return json.dumps(release())
            self.assertEqual(args, ("release", "download", "v0.1.0", "--repo", "Georicl/seqviz-rs",
                                    "--pattern", "SHA256SUMS", "--output", "-"))
            return checksum_text()

        with tempfile.TemporaryDirectory() as tmp, patch.object(updater, "gh", side_effect=gh):
            formula = Path(tmp) / "Formula/seqviz-rs.rb"
            with patch.object(updater, "FORMULA", formula):
                self.assertTrue(updater.update("v0.1.0"))
                expected = updater.render_formula("v0.1.0", updater.parse_checksums(checksum_text()))
                self.assertEqual(formula.read_text(), expected)
                self.assertFalse(updater.update("v0.1.0"))

    def test_draft_is_rejected_before_download(self):
        metadata = release()
        metadata["draft"] = True
        with patch.object(updater, "gh", return_value=json.dumps(metadata)) as gh:
            with self.assertRaises(ValueError):
                updater.update("v0.1.0")
            self.assertEqual(gh.call_count, 1)

    def test_prerelease_tag_is_rejected(self):
        with self.assertRaises(ValueError):
            updater.render_formula("v0.2.0-rc1", {})


if __name__ == "__main__":
    unittest.main()
