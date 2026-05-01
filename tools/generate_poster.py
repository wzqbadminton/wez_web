"""Generate a printable poster (PDF) for WZQ Badminton Club.

Outputs: poster_wzq.pdf at letter size (8.5 x 11 in), portrait.
Includes a large centered QR code linking to https://wzqbadminton.com/.
"""
from io import BytesIO
from pathlib import Path

import qrcode
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
URL = "https://wzqbadminton.com/"
OUT = ROOT / "poster_wzq.pdf"
LOGO = ROOT / "logo.jpg"

# Brand colors
COURT = HexColor("#1f7a4d")
COURT_DARK = HexColor("#0f3d2a")
ACCENT = HexColor("#e63946")
INK = HexColor("#14181f")
INK_SOFT = HexColor("#5a6271")
CREAM = HexColor("#faf7f0")
LINE = HexColor("#e3dfd5")
MINT = HexColor("#9bd9b6")

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
CJK = "STSong-Light"


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

    # ----- Background -----
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ----- Top accent bar -----
    c.setFillColor(ACCENT)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)

    # ----- Header (logo + brand, top corners) -----
    header_y = H - 0.75 * inch

    if LOGO.exists():
        s = 0.55 * inch
        c.drawImage(
            str(LOGO),
            0.7 * inch, header_y - s / 2 + 0.05 * inch,
            width=s, height=s,
            mask="auto", preserveAspectRatio=True,
        )

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(1.4 * inch, header_y + 0.05 * inch, "WZQ BADMINTON CLUB")
    c.setFillColor(INK_SOFT)
    c.setFont("Helvetica", 9)
    c.drawString(1.4 * inch, header_y - 0.13 * inch, "POMONA, CA  ·  EST.")

    c.setFillColor(COURT)
    c.setFont(CJK, 12)
    c.drawRightString(W - 0.7 * inch, header_y + 0.02 * inch, "羽毛球俱乐部")

    # ----- Title block -----
    title_y = H - 1.95 * inch

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, title_y + 0.55 * inch, "—  P R O F E S S I O N A L   B A D M I N T O N  —")

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 56)
    c.drawCentredString(W / 2, title_y, "TRAIN LIKE")
    c.setFillColor(COURT)
    c.drawCentredString(W / 2, title_y - 0.7 * inch, "A CHAMPION")

    line_w = 1.2 * inch
    c.setFillColor(ACCENT)
    c.rect((W - line_w) / 2, title_y - 0.95 * inch, line_w, 4, fill=1, stroke=0)

    c.setFillColor(INK_SOFT)
    c.setFont(CJK, 13)
    c.drawCentredString(W / 2, title_y - 1.3 * inch, "由原中国羽毛球退役运动员创办  ·  BWF 与 USAB 双认证")
    c.drawCentredString(W / 2, title_y - 1.55 * inch, "儿童  ·  青少年  ·  成人  专业培训")

    # ----- Feature pills (between tagline and QR) -----
    feat_y = title_y - 2.0 * inch
    features = [
        ("10+", "年教学经验"),
        ("BWF", "世界羽联认证"),
        ("U7-U18", "全年龄培训"),
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
        c.setFont(CJK, 9)
        c.drawCentredString(x + pill_w / 2, feat_y - 0.58 * inch, small)

    # ----- QR card (focal point) -----
    qr_size = 2.4 * inch
    qr_x = (W - qr_size) / 2
    qr_y = 2.4 * inch

    pad = 0.3 * inch
    label_h = 0.7 * inch
    card_x = qr_x - pad
    card_y = qr_y - label_h - pad
    card_w = qr_size + 2 * pad
    card_h = qr_size + label_h + 2 * pad

    # Soft shadow
    c.setFillColor(HexColor("#d6d2c5"))
    c.roundRect(card_x + 5, card_y - 5, card_w, card_h, 14, fill=1, stroke=0)
    # Card
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.roundRect(card_x, card_y, card_w, card_h, 14, fill=1, stroke=1)

    # QR
    c.drawImage(make_qr(URL), qr_x, qr_y, width=qr_size, height=qr_size, mask="auto")

    # Labels under QR
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, qr_y - 0.3 * inch, "S C A N   T O   V I S I T")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, qr_y - 0.58 * inch, "wzqbadminton.com")

    # Below card hint (Chinese)
    c.setFillColor(INK_SOFT)
    c.setFont(CJK, 10)
    c.drawCentredString(W / 2, card_y - 0.28 * inch, "扫描二维码  ·  访问官网  ·  在线报名")

    # ----- Feature pills (between QR and contact band) [REMOVED - moved up] -----

    # ----- Bottom contact band -----
    band_h = 1.45 * inch
    c.setFillColor(COURT_DARK)
    c.rect(0, 0, W, band_h, fill=1, stroke=0)

    cy = band_h - 0.35 * inch

    # Left column
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

    # Right column
    rx = W - 0.7 * inch
    c.setFillColor(MINT)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(rx, cy, "REGISTER")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 13)
    c.drawRightString(rx, cy - 0.22 * inch, "app.wzqbadminton.com")

    c.setFillColor(MINT)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(rx, cy - 0.55 * inch, "FOLLOW")
    c.setFillColor(white)
    c.setFont("Helvetica", 11)
    c.drawRightString(rx, cy - 0.75 * inch, "@wzqbadmintonclub")

    # Red bottom strip
    strip_h = 0.32 * inch
    c.setFillColor(ACCENT)
    c.rect(0, 0, W, strip_h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(CJK, 11)
    c.drawCentredString(W / 2, strip_h / 2 - 4, "立即扫码  ·  报名试课  ·  开启羽毛球之旅")

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    draw_poster()
