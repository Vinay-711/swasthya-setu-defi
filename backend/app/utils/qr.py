import base64
from io import BytesIO

import qrcode


def build_qr_png_bytes(content: str) -> bytes:
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(content)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def build_qr_data_url(content: str) -> str:
    png_bytes = build_qr_png_bytes(content)
    encoded = base64.b64encode(png_bytes).decode()
    return f"data:image/png;base64,{encoded}"
