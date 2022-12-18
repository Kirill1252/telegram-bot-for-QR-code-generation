import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import ImageColorMask
from PIL import Image


def qr_code(data, img):
    logo = Image.open(img)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H
                       , version=3
                       , border=2
                       , box_size=18,
                       )
    qr.add_data(data)
    qr_img = qr.make_image(image_factory=StyledPilImage, fill_color=(55, 95, 35),
                           color_mask=ImageColorMask(back_color=(255, 255, 255), color_mask_image=logo), )
    qr_img.save('qr_code.png')

    return qr_img
