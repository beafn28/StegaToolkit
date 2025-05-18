from PIL import Image, ImageChops, ImageEnhance
import io
import base64

def generar_ela(imagen: Image.Image, calidad_jpeg: int = 90) -> str:
    """
    Genera la imagen ELA (Error Level Analysis) a partir de una imagen RGB.
    Retorna una cadena base64 de la imagen ELA en formato PNG.
    """
    # Guardar en JPEG con calidad controlada (simula compresión)
    jpeg_io = io.BytesIO()
    imagen.save(jpeg_io, 'JPEG', quality=calidad_jpeg)
    jpeg_io.seek(0)
    recomprimida = Image.open(jpeg_io)

    # Calcular diferencia entre original y recomprimida
    ela_img = ImageChops.difference(imagen, recomprimida)

    # Escalar contraste para visualizar mejor las diferencias
    extrema = ela_img.getextrema()
    max_diff = max([ex[1] for ex in extrema]) or 1
    escala = 255.0 / max_diff
    ela_img = ImageEnhance.Brightness(ela_img).enhance(escala)

    # Convertir la imagen a base64 para frontend
    buffer = io.BytesIO()
    ela_img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")
