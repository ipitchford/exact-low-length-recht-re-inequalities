#!/usr/bin/env python3
"""Enforce the anonymous, single-paper, portable publication surface."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
EXPECTED_SOURCE = PAPER / "exact_low_length_recht_re.tex"
EXPECTED_PDF = PAPER / "exact_low_length_recht_re.pdf"
TEXT_SUFFIXES = {
    ".cff",
    ".json",
    ".md",
    ".py",
    ".sha256",
    ".sh",
    ".tex",
    ".time",
    ".txt",
}
LOCAL_PATH_PATTERNS = (
    (
        "macOS home path",
        re.compile(r"(?<![A-Za-z0-9:])/" + r"Users/"),
    ),
    (
        "Linux home path",
        re.compile(r"(?<![A-Za-z0-9:])/" + r"home/"),
    ),
    (
        "macOS temporary path",
        re.compile(r"(?<![A-Za-z0-9:])/" + r"private/var/folders/"),
    ),
    (
        "Windows home path",
        re.compile(r"(?i)\b[A-Z]:[\\/]+" + r"Users[\\/]"),
    ),
    (
        "local file URI",
        re.compile(r"file" + r"://", re.IGNORECASE),
    ),
)
IDENTITY_COMMANDS = (
    r"\address",
    r"\affil",
    r"\affiliation",
    r"\email",
    r"\orcid",
    r"\thanks",
)
IGNORED_PARTS = {".git", ".pytest_cache", ".venv", "__pycache__"}


def ignored(path: Path) -> bool:
    """Return whether ``path`` is outside the packaged publication payload."""

    relative = path.relative_to(ROOT)
    return any(part in IGNORED_PARTS for part in relative.parts)


def pdf_literal(data: bytes, opening: int) -> tuple[bytes, int]:
    """Decode one PDF literal string beginning at ``opening``."""

    if data[opening : opening + 1] != b"(":
        raise ValueError("PDF literal does not begin with '('")
    output = bytearray()
    depth = 1
    index = opening + 1
    simple_escapes = {
        ord("n"): ord("\n"),
        ord("r"): ord("\r"),
        ord("t"): ord("\t"),
        ord("b"): ord("\b"),
        ord("f"): ord("\f"),
        ord("("): ord("("),
        ord(")"): ord(")"),
        ord("\\"): ord("\\"),
    }
    while index < len(data):
        value = data[index]
        index += 1
        if value == ord("\\"):
            if index >= len(data):
                raise ValueError("truncated PDF escape")
            escaped = data[index]
            index += 1
            if escaped in simple_escapes:
                output.append(simple_escapes[escaped])
            elif ord("0") <= escaped <= ord("7"):
                digits = bytearray([escaped])
                while (
                    len(digits) < 3
                    and index < len(data)
                    and ord("0") <= data[index] <= ord("7")
                ):
                    digits.append(data[index])
                    index += 1
                output.append(int(digits.decode("ascii"), 8))
            elif escaped == ord("\r"):
                if index < len(data) and data[index] == ord("\n"):
                    index += 1
            elif escaped == ord("\n"):
                continue
            else:
                output.append(escaped)
        elif value == ord("("):
            depth += 1
            output.append(value)
        elif value == ord(")"):
            depth -= 1
            if depth == 0:
                return bytes(output), index
            output.append(value)
        else:
            output.append(value)
    raise ValueError("unterminated PDF literal")


def decode_pdf_text(value: bytes) -> str:
    if value.startswith(b"\xfe\xff"):
        return value[2:].decode("utf-16-be")
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError:
        return value.decode("latin-1")


def pdf_authors(data: bytes) -> list[str]:
    authors: list[str] = []
    for match in re.finditer(br"/Author\s*\(", data):
        value, _ = pdf_literal(data, match.end() - 1)
        authors.append(decode_pdf_text(value))
    return authors


def path_leaks(text: str) -> list[str]:
    return [
        label
        for label, pattern in LOCAL_PATH_PATTERNS
        if pattern.search(text)
    ]


def main() -> int:
    failures: list[str] = []
    sources = sorted(path for path in ROOT.rglob("*.tex") if not ignored(path))
    pdfs = sorted(path for path in ROOT.rglob("*.pdf") if not ignored(path))
    if sources != [EXPECTED_SOURCE]:
        failures.append(
            "paper sources must be exactly "
            f"[{EXPECTED_SOURCE.relative_to(ROOT)}], found "
            f"{[path.relative_to(ROOT).as_posix() for path in sources]}"
        )
    if pdfs != [EXPECTED_PDF]:
        failures.append(
            "paper PDFs must be exactly "
            f"[{EXPECTED_PDF.relative_to(ROOT)}], found "
            f"{[path.relative_to(ROOT).as_posix() for path in pdfs]}"
        )

    if EXPECTED_SOURCE.is_file():
        source = EXPECTED_SOURCE.read_text(encoding="utf-8")
        authors = re.findall(r"\\author\s*\{([^{}]*)\}", source)
        if authors != ["Anonymous"]:
            failures.append(
                f"TeX author declarations are {authors!r}, expected ['Anonymous']"
            )
        metadata_authors = re.findall(
            r"pdfauthor\s*=\s*\{([^{}]*)\}",
            source,
        )
        if metadata_authors != ["Anonymous"]:
            failures.append(
                "TeX PDF-author metadata must occur exactly once as Anonymous"
            )
        preamble = source.split(r"\begin{document}", 1)[0]
        disclosed_commands = [
            command for command in IDENTITY_COMMANDS if command in preamble
        ]
        if disclosed_commands:
            failures.append(
                "identity-bearing preamble commands present: "
                + ", ".join(disclosed_commands)
            )

    if EXPECTED_PDF.is_file():
        data = EXPECTED_PDF.read_bytes()
        if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-1024:]:
            failures.append("paper PDF lacks a valid header or terminal EOF marker")
        try:
            authors = pdf_authors(data)
        except (UnicodeDecodeError, ValueError) as exc:
            failures.append(f"paper PDF author metadata is unreadable: {exc}")
        else:
            if authors != ["Anonymous"]:
                failures.append(
                    f"paper PDF author metadata is {authors!r}, "
                    "expected ['Anonymous']"
                )
        pdf_probe = data.decode("latin-1")
        for leak in path_leaks(pdf_probe):
            failures.append(f"paper PDF contains a {leak}")

    for path in sorted(ROOT.rglob("*")):
        if (
            not path.is_file()
            or ignored(path)
            or path.suffix.lower() not in TEXT_SUFFIXES
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(
                f"{path.relative_to(ROOT)}: declared text file is not UTF-8"
            )
            continue
        for leak in path_leaks(text):
            failures.append(f"{path.relative_to(ROOT)}: contains a {leak}")

    if failures:
        print("PUBLICATION SHAPE: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(
        "PUBLICATION SHAPE: PASS "
        "(one TeX, one PDF, Anonymous metadata, no local paths)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
