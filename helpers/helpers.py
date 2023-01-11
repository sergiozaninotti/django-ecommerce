from django.conf import settings
from PIL import Image
import os


def formata_preco(val):
    return f'R${val:.2f}'.replace('.', ',')


def cart_total_items(cart):
    return sum([item['quantidade'] for item in cart.values()])


def cart_total_value(cart):
    return sum(
        [
            item.get('preco_quantitativo_promo')
            if item.get('preco_quantitativo_promo')
            else item.get('preco_quantitativo')
            for item
            in cart.values()
        ]
    )


def resize_image(img, new_width, name=None, extension=None):
    img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
    img_pil = Image.open(img_full_path)

    if not img_pil.mode == 'RGB':
        img_pil = img_pil.convert('RGB')

    original_width, original_height = img_pil.size
    new_height = round((new_width * original_height) / original_width)

    if original_width <= new_width:
        img_pil.close()
        return

    new_image = img_pil.resize((new_width, new_height), Image.LANCZOS)

    if name:
        img_name, ext = img_full_path.split('.').pop().split('.')
        img_full_path = img_full_path.replace(img_name + '.' + ext, name + '.' + ext)

    if extension:
        ext = img_full_path.split('.')[-1]
        img_full_path = img_full_path.replace('.' + ext, '.' + extension)

    new_image.save(
        img_full_path,
        optimize=True,
        quality=70
    )

    img_pil.close()
