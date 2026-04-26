import tempfile
import unittest
from pathlib import Path

from numberlink.file_io.loader import load_text


class TestLoader(unittest.TestCase):
    def test_load_text_reads_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "puzzle.txt"
            file_path.write_text(
                "hex\nA . .\n. B .\nA . B\n",
                encoding="utf-8",
            )

            result = load_text(file_path)

        self.assertEqual(result, "hex\nA . .\n. B .\nA . B\n")


if __name__ == "__main__":
    unittest.main()
