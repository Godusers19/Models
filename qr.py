# meta developer: @Goduser18
from .. import loader, utils
import qrcode
import os
from io import BytesIO
from PIL import Image

@loader.tds
class QRCodeMod(loader.Module):
    strings = {"name": "QRCode"}

    async def qrcmd(self, message):
        """Создать qr. Используй: .qr <текст или ссылка>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Пожалуйста, укажи текст или ссылку для QR-кода. Пример: .qr https://example.com")
            return

        await utils.answer(message, "Генерирую QR-код...")

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(args)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            await message.client.send_file(
                message.chat_id,
                buffer,
                caption=f"QR-код для: {args}",
                reply_to=message.id
            )

            await message.delete()

        except Exception as e:
            await utils.answer(message, f"Ошибка при создании QR-кода: {str(e)}")