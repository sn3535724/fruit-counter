from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any, Mapping, Sequence

from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


FIELDS = ["timestamp", "apple", "banana", "orange", "total"]
HEADERS = ["Дата и время (МСК)", "Яблоки", "Бананы", "Апельсины", "Всего"]
PDF_FONT = "Helvetica"

for font_path in (
    Path("C:/Windows/Fonts/arial.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
):
    if font_path.exists():
        pdfmetrics.registerFont(TTFont("ReportFont", str(font_path)))
        PDF_FONT = "ReportFont"
        break


def _rows(history: Sequence[Mapping[str, Any]]) -> list[list[Any]]:
    return [
        [entry.get(column, "") for column in FIELDS]
        for entry in history
    ]


def export_pdf(history: Sequence[Mapping[str, Any]]) -> BytesIO:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )
    table_data = [HEADERS, *_rows(history)]
    table = Table(table_data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), PDF_FONT),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )
    document.build([table])
    buffer.seek(0)
    return buffer


def export_excel(history: Sequence[Mapping[str, Any]]) -> BytesIO:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "История"
    worksheet.append(HEADERS)
    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    for row in _rows(history):
        worksheet.append(row)

    worksheet.freeze_panes = "A2"
    widths = {"A": 25, "B": 12, "C": 12, "D": 12, "E": 12}
    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer
