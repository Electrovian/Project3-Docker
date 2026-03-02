#!/usr/bin/env python3
from __future__ import annotations

import re
import socket
from collections import Counter
from pathlib import Path
from typing import List


DATA_DIR = Path("/home/data")
OUTPUT_DIR = DATA_DIR / "output"
RESULT_FILE = OUTPUT_DIR / "result.txt"

FILE_IF = DATA_DIR / "IF.txt"
FILE_ALWAYS = DATA_DIR / "AlwaysRememberUsThisWay.txt"


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def tokenize_basic(text: str) -> List[str]:
    """
    Basic tokenizer for general word counting.
    Keeps contractions as one token (e.g., don't) for normal counting.
    """
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())


def tokenize_split_contractions(text: str) -> List[str]:
    """
    Tokenizer that splits contractions by treating apostrophes as separators.
    Example: "I'm" -> ["i", "m"], "don't" -> ["don", "t"]
    This matches the requirement to split contractions into individual words.
    """
    text = text.lower().replace("â€™", "'").replace("\u2019", "'")
    text = text.replace("'", " ")
    return re.findall(r"[A-Za-z]+", text)


def word_count(tokens: List[str]) -> int:
    return len(tokens)


def top_n(tokens: List[str], n: int = 3) -> List[tuple[str, int]]:
    counts = Counter(tokens)
    # Sort by frequency desc, then alphabetically asc for deterministic output
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:n]


def detect_container_ip() -> str:
    """
    Best-effort IP detection inside container.
    Uses a UDP socket trick to get the primary outbound interface IP.
    Falls back to hostname resolution.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))
            # This infers the active interface IP without requiring internet access.
            return s.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "Unable to determine IP address"


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    ensure_output_dir()

    text_if = read_text_file(FILE_IF)
    text_always = read_text_file(FILE_ALWAYS)

    # a) total words in each file (standard tokenization)
    tokens_if = tokenize_basic(text_if)
    tokens_always_basic = tokenize_basic(text_always)

    count_if = word_count(tokens_if)
    count_always = word_count(tokens_always_basic)

    # b) grand total
    grand_total = count_if + count_always

    # c) top 3 frequent words in IF.txt
    top3_if = top_n(tokens_if, 3)

    # d) split contractions for AlwaysRememberUsThisWay.txt, then top 3
    tokens_always_split = tokenize_split_contractions(text_always)
    top3_always_split = top_n(tokens_always_split, 3)

    # e) IP address of machine running the container
    ip_addr = detect_container_ip()

    # f) write results to /home/data/output/result.txt and print contents
    lines = []
    lines.append("Docker Text Processing Results")
    lines.append("=" * 32)
    lines.append("")
    lines.append(f"1) Total words in IF.txt: {count_if}")
    lines.append(f"2) Total words in AlwaysRememberUsThisWay.txt: {count_always}")
    lines.append(f"3) Grand total words across both files: {grand_total}")
    lines.append("")

    lines.append("4) Top 3 most frequent words in IF.txt:")
    for word, cnt in top3_if:
        lines.append(f"   - {word}: {cnt}")
    lines.append("")

    lines.append("5) Top 3 most frequent words in AlwaysRememberUsThisWay.txt")
    lines.append("   (with contractions split into individual words):")
    for word, cnt in top3_always_split:
        lines.append(f"   - {word}: {cnt}")
    lines.append("")

    lines.append(f"6) Container IP address: {ip_addr}")
    lines.append("")

    result_text = "\n".join(lines) + "\n"
    RESULT_FILE.write_text(result_text, encoding="utf-8")

    print(result_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
