"""Generate English-only poster (PDF) for WZQ Badminton Club.

Outputs: poster_wzq_en.pdf at letter size, portrait.
"""
from io import BytesIO
from pathlib import Path

import qrcode
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
URL = "https://wzqbadminton.com/"
OUT = ROOT / "poster_wzq_en.pdf"
LOGO = ROOT / "logo.jpg"

COURT = HexColor("#1f7a4d")
COURT_DARK = HexColor("#0f3d2a")
ACCENT = HexColor("#e63946")
INK = HexColor("#14181f")
INK_SOFT = HexColor("#5a6271")
CREAM = HexColor("#faf7f0")
LINE = HexColor("#e3dfd5")
MINT = HexColor("#9bd9b6")


def make_qr(data: str) -> ImageReader:
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f3d2a", back_color="white").convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def draw_poster() -> None:
    W, H = letter  # 612 x 792 pt
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("WZQ Badminton Club")
    c.setAuthor("WZQ Badminton Club")

    # Background
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Top accent bar
    c.setFillColor(ACCENT)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)

    # ===== Header =====
    header_y = H - 0.75 * inch
    if LOGO.exists():
        s = 0.55 * inch
        c.drawImage(
            str(LOGO),
            0.7 * inch, header_y - s / 2 + 0.05 * inch,
            width=s, height=s, mask="auto", preserveAspectRatio=True,
        )
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(1.4 * inch, header_y + 0.05 * inch, "WZQ BADMINTON CLUB")
    c.setFillColor(INK_SOFT)
    c.setFont("Helvetica", 9)
    c.drawString(1.4 * inch, header_y - 0.13 * inch, "POMONA, CALIFORNIA")

    c.setFillColor(COURT)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - 0.7 * inch, header_y + 0.02 * inch, "PROFESSIONAL  COACHING")

    # ===== Main title =====
    title_y = H - 2.05 * inch

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, title_y + 0.85 * inch, "—  E L I T E   B A D M I N T O N   T R A I N I N G  —")

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 60)
    c.drawCentredString(W / 2, title_y, "TRAIN LIKE")
    c.setFillColor(COURT)
    c.drawCentredString(W / 2, title_y - 0.78 * inch, "A CHAMPION")

    # Underline accent
    line_w = 1.2 * inch
    c.setFillColor(ACCENT)
    c.rect((W - line_w) / 2, title_y - 1.05 * inch, line_w, 4, fill=1, stroke=0)

    # English tagline
    c.setFillColor(INK_SOFT)
    c.setFont("Helvetica", 13)
    c.drawCentredString(W / 2, title_y - 1.4 * inch, "Founded by a former Chinese national badminton athlete.")
    c.drawCentredString(W / 2, title_y - 1.62 * inch, "BWF and USAB certified coaches  ·  Juniors  ·  Teens  ·  Adults")

    # ===== Feature pills =====
    feat_y = title_y - 2.05 * inch
    features = [
        ("10+", "YEARS COACHING"),
        ("BWF", "WORLD-CERTIFIED"),
        ("U7-U18", "ALL AGE GROUPS"),
    ]
    pill_w = 1.7 * inch
    pill_h = 0.7 * inch
    gap = 0.18 * inch
    total = pill_w * 3 + gap * 2
    sx = (W - total) / 2
    for i, (big, small) in enumerate(features):
        x = sx + i * (pill_w + gap)
        c.setFillColor(white)
        c.setStrokeColor(COURT)
        c.setLineWidth(1.5)
        c.roundRect(x, feat_y - pill_h, pill_w, pill_h, 8, fill=1, stroke=1)
        c.setFillColor(COURT_DARK)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(x + pill_w / 2, feat_y - 0.34 * inch, big)
        c.setFillColor(INK_SOFT)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + pill_w / 2, feat_y - 0.55 * inch, small)

    # ===== QR card =====
    qr_size = 2.4 * inch
    qr_x = (W - qr_size) / 2
    qr_y = 2.4 * inch

    pad = 0.3 * inch
    label_h = 0.7 * inch
    card_x = qr_x - pad
    card_y = qr_y - label_h - pad
    card_w = qr_size + 2 * pad
    card_h = qr_size + label_h + 2 * pad

    c.setFillColor(HexColor("#d6d2c5"))
    c.roundRect(card_x + 5, card_y - 5, card_w, card_h, 14, fill=1, stroke=0)
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.roundRect(card_x, card_y, card_w, card_h, 14, fill=1, stroke=1)

    c.drawImage(make_qr(URL), qr_x, qr_y, width=qr_size, height=qr_size, mask="auto")

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, qr_y - 0.3 * inch, "S C A N   T O   V I S I T")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, qr_y - 0.58 * inch, "wzqbadminton.com")

    c.setFillColor(INK_SOFT)
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, card_y - 0.22 * inch, "Visit our website  ·  Register online  ·  See class schedule")

    # ===== Bottom contact band =====
    band_h = 1.45 * inch
    c.setFillColor(COURT_DARK)
    c.rect(0, 0, W, band_h, fill=1, stroke=0)

    cy = band_h - 0.35 * inch

    c.setFillColor(MINT)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.7 * inch, cy, "CALL")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.7 * inch, cy - 0.22 * inch, "626-265-5766")

    c.setFillColor(MINT)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.7 * inch, cy - 0.55 * inch, "LOCATION")
    c.setFillColor(white)
    c.setFont("Helvetica", 11)
    c.drawString(0.7 * inch, cy - 0.75 * inch, "2780 S Reservoir St, Pomona, CA")

    rx = W - 0.7 * inch
    c.setFillColor(MINT)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(rx, cy, "REGISTER ONLINE")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 13)
    c.drawRightString(rx, cy - 0.22 * inch, "app.wzqbadminton.com")

    c.setFillColor(MINT)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(rx, cy - 0.55 * inch, "FOLLOW")
    c.setFillColor(white)
    c.setFont("Helvetica", 11)
    c.drawRightString(rx, cy - 0.75 * inch, "@wzqbadmintonclub")

    # Red strip
    strip_h = 0.32 * inch
    c.setFillColor(ACCENT)
    c.rect(0, 0, W, strip_h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, strip_h / 2 - 4, "S C A N   ·   R E G I S T E R   ·   T R A I N   ·   C O M P E T E   ·   W I N")

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    draw_poster()
