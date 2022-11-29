import bz2
import gzip
import random
import string

import brotli
import fire
from rich.console import Console
from rich.table import Table
from zstandard import ZstdCompressor, ZstdDecompressor

from standards import CompressionStandard
from timer import MeasureExecutionTime


class Comparator:
    """
    Simple comparator of compression standards.

    Currently supported standards: gzip, bz2, brotli, zstd.
    """

    def __init__(self, standards: list[CompressionStandard] | None = None):
        self.default_standards = [
            CompressionStandard(
                name="gzip", compressor=gzip.compress, decompressor=gzip.decompress
            ),
            CompressionStandard(
                name="bz2",
                compressor=bz2.compress,
                decompressor=bz2.decompress,
            ),
            CompressionStandard(
                name="brotli (google)",
                compressor=brotli.compress,
                decompressor=brotli.decompress,
            ),
            CompressionStandard(
                name="zstd (facebook)",
                compressor=ZstdCompressor().compress,
                decompressor=ZstdDecompressor().decompress,
            ),
        ]
        self._standards = standards

    @property
    def standards(self) -> list[CompressionStandard]:
        return self._standards or self.default_standards

    @staticmethod
    def compare_compression(data: bytes, standards: list[CompressionStandard]):
        table = Table(title=f"Data of length {len(data)}")
        table.add_column("Standard name", max_width=60)
        table.add_column("Compressed size")
        table.add_column("Compression time")
        table.add_column("Decompression time")

        for standard in standards:
            with MeasureExecutionTime(standard.name) as compression_timer:
                compressed = standard.compressor(data)
            with MeasureExecutionTime(standard.name) as decompression_timer:
                decompressed = standard.decompressor(compressed)
            assert (
                decompressed == data
            ), "Decompressed data is different from original data"
            table.add_row(
                standard.name,
                str(len(compressed)),
                str(compression_timer.execution_time),
                str(decompression_timer.execution_time),
            )

        console = Console()
        console.print(table)

    def compare_unified(self, length: int) -> None:
        """
        Compare unified data with given length
        """
        data = b"a" * length
        self.compare_compression(data, standards=self.standards)

    def compare_random(self, length: int) -> None:
        """
        Compare random data with given length
        """
        data = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=length)
        ).encode()
        self.compare_compression(data, standards=self.standards)

    def compare_file(self, path: str) -> None:
        with open(path, "rb") as file:
            data = file.read()
            self.compare_compression(data, standards=self.standards)


if __name__ == "__main__":
    fire.Fire(Comparator)
