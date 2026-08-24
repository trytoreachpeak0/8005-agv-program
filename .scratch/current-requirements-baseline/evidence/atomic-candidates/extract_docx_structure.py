from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table
from docx.text.paragraph import Paragraph


def iter_blocks(parent: DocumentObject):
    body = parent.element.body
    for child in body.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, parent)
        elif child.tag.endswith("}tbl"):
            yield Table(child, parent)


def clean(value: str) -> str:
    return " ".join(value.replace("\t", " ").split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    args = parser.parse_args()

    document = Document(args.docx)
    paragraph_no = 0
    table_no = 0
    for block in iter_blocks(document):
        if isinstance(block, Paragraph):
            paragraph_no += 1
            text = clean(block.text)
            if text:
                print(f"P{paragraph_no:04d}\t{clean(block.style.name)}\t{text}")
            continue

        table_no += 1
        for row_no, row in enumerate(block.rows, start=1):
            cells = [clean(cell.text) for cell in row.cells]
            print(f"T{table_no:02d}R{row_no:03d}\tTABLE\t{' | '.join(cells)}")


if __name__ == "__main__":
    main()
