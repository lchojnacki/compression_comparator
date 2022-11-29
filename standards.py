from dataclasses import dataclass
from typing import Callable


@dataclass
class CompressionStandard:
    name: str
    compressor: Callable
    decompressor: Callable
