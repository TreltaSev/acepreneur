import qrcode.constants
from quart import send_file
from utils.package import cloakquart
import qrcode
from io import BytesIO
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styledpil import StyledPilImage
from PIL import Image
from siblink import Config


blueprint = cloakquart.Blueprint("api:@qrcode", __name__)


@blueprint.route("/api/qr/<data>", methods=["GET"])
# @getHeaders(["Bearer"], explicit=True)    
# @getUser()
async def qr_GET(data, *args, **kwargs):
    
    if (len(data) > 150):
        return "Data too large", 413
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)

    _qrcode = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(1))
    _qrcode_img = _qrcode.convert("RGBA")

    _logo = Image.open((Config.root / "../assets/logo/4x_qr_sec.png").absolute()).convert("RGBA")
    width, height = _qrcode_img.size

    logo_size = int(width * 0.28)
    _logo = _logo.resize((logo_size, logo_size), Image.LANCZOS)

    _qrcode_with_logo = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    _qrcode_with_logo.paste(_qrcode_img, (0, 0))

    xmin = ymin = int((width / 2) - (logo_size / 2))

    _qrcode_with_logo.paste(_logo, (xmin, ymin), _logo)

    buf = BytesIO()
    _qrcode_with_logo.save(buf, format="PNG")
    buf.seek(0)
    
    return await send_file(buf, mimetype="image/png")
