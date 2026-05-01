"""Generate a printable poster (PDF) for WZQ Badminton Club.

Outputs: poster_wzq.pdf at letter size (8.5 x 11 in), portrait.
Includes a QR code linking to https://wzqbadminton.com/.
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

# Brand colors (match the site)
COURT = HexColor("#1f7a4d")
COURT_DARK = HexColor("#14533a")
ACCENT = HexColor("#e63946")
INK = HexColor("#14181f")
INK_SOFT = HexColor("#4a5160")
BG = HexColor("#f7f5f0")
LINE = HexColor("#e7e3da")

# Register a CJK-capable font for Chinese
pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
CJK = "STSong-Light"


def make_qr(data: str, box_size: int = 14, border: int = 2) -> ImageReader:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#14181f", back_color="white").convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def draw_poster() -> None:
    W, H = letter  # 612 x 792 pt
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("WZQ Badminton Club Poster")
    c.setAuthor("WZQ Badminton Club")

    # ---- Background ----
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ---- Top hero band (green) ----
    hero_h = 3.2 * inch
    c.setFillColor(COURT_DARK)
    c.rect(0, H - hero_h, W, hero_h, fill=1, stroke=0)

    # Subtle court grid lines
    c.setStrokeColor(HexColor("#1f7a4d"))
    c.setLineWidth(0.5)
    for i in range(0, int(W), 30):
        c.line(i, H - hero_h, i, H)
    for j in range(0, int(hero_h), 30):
        c.line(0, H - j, W, H - j)

    # Red accent bar at bottom of hero
    c.setFillColor(ACCENT)
    c.rect(0, H - hero_h - 8, W, 8, fill=1, stroke=0)

    # ---- Logo ----
    if LOGO.exists():
        logo_size = 1.0 * inch
        c.drawImage(
            str(LOGO),
            (W - logo_size) / 2,
            H - 1.0 * inch - logo_size / 2,
            width=logo_size,
            height=logo_size,
            mask="auto",
            preserveAspectRatio=True,
        )

    # ---- Hero title ----
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 2.55 * inch, "WZQ BADMINTON")
    c.setFont("Helvetica", 13)
    c.setFillColor(HexColor("#ffd9dc"))
    c.drawCentredString(W / 2, H - 2.85 * inch, "PROFESSIONAL BADMINTON COACHING  ·  POMONA, CA")

    # ---- Chinese subtitle (below hero, on cream) ----
    y = H - hero_h - 0.55 * inch
    c.setFillColor(INK)
    c.setFont(CJK, 22)
    c.drawCentredString(W / 2, y, "WZQ 羽毛球俱乐部")
    y -= 26
    c.setFont(CJK, 12)
    c.setFillColor(INK_SOFT)
    c.drawCentredString(W / 2, y, "由原中国羽毛球退役运动员创办  ·  BWF 与 USAB 双认证教练团队")
    y -= 18
    c.drawCentredString(W / 2, y, "儿童 · 青少年 · 成人羽毛球专业培训")

    # ---- Feature row (3 chips) ----
    y -= 38
    chips = ["10+ 年教学经验", "BWF 世界羽联认证", "U7 – U18 全年龄段"]
    chip_w = 1.95 * inch
    chip_h = 0.45 * inch
    gap = 0.15 * inch
    total_w = chip_w * 3 + gap * 2
    x0 = (W - total_w) / 2
    c.setFont(CJK, 11)
    for i, label in enumerate(chips):
        cx = x0 + i * (chip_w + gap)
        c.setFillColor(white)
        c.setStrokeColor(LINE)
        c.setLineWidth(1)
        c.roundRect(cx, y - chip_h, chip_w, chip_h, 8, fill=1, stroke=1)
        c.setFillColor(COURT)
        c.drawCentredString(cx + chip_w / 2, y - chip_h + 14, label)

    # ---- QR code block (centered, the focal point) ----
    qr_size = 3.2 * inch
    qr_x = (W - qr_size) / 2
    qr_y = 1.85 * inch

    # White card behind QR
    pad = 0.35 * inch
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    card_x = qr_x - pad
    card_y = qr_y - pad - 0.45 * inch
    card_w = qr_size + 2 * pad
    card_h = qr_size + 2 * pad + 0.45 * inch
    c.roundRect(card_x, card_y, card_w, card_h, 16, fill=1, stroke=1)

    # QR
    c.drawImage(make_qr(URL), qr_x, qr_y, width=qr_size, height=qr_size, mask="auto")

    # URL under QR
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W / 2, qr_y - 0.28 * inch, "wzqbadminton.com")

    # "Scan to learn more" label above the card
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, card_y + card_h + 14, "SCAN TO VISIT  ·  扫码访问官网")

    # ---- Contact strip ----
    cy = 1.35 * inch
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W / 2, cy, "📞 626-265-5766    ✍ app.wzqbadminton.com")
    cy -= 20
    c.setFont(CJK, 11)
    c.setFillColor(INK_SOFT)
    c.drawCentredString(W / 2, cy, "地址: 2780 S Reservoir St, Pomona, CA  ·  Instagram: @wzqbadmintonclub")

    # ---- Bottom red banner ----
    band_h = 0.75 * inch
    c.setFillColor(ACCENT)
    c.rect(0, 0, W, band_h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(CJK, 16)
    c.drawCentredString(W / 2, band_h / 2 + 4, "立即扫码 · 报名试课 · 开启羽毛球之旅")
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, band_h / 2 - 12, "TRAIN  ·  COMPETE  ·  WIN")

    c.showPage()
    c.save()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    draw_poster()
