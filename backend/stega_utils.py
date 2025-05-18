from PIL import Image

# Marcador especial al inicio del mensaje para detectar si realmente hay texto oculto válido
MARCADOR = "STEG:"

def ocultar_mensaje_en_imagen(img: Image.Image, mensaje: str) -> Image.Image:
    """
    Oculta un mensaje en una imagen usando LSB. El mensaje se marca con 'STEG:' al inicio.
    """
    mensaje_completo = MARCADOR + mensaje
    binario = ''.join([format(byte, '08b') for byte in mensaje_completo.encode('utf-8')]) + '00000000'

    datos = list(img.convert('RGB').getdata())
    nuevos_datos = []
    i = 0
    for r, g, b in datos:
        if i < len(binario): r = (r & ~1) | int(binario[i]); i += 1
        if i < len(binario): g = (g & ~1) | int(binario[i]); i += 1
        if i < len(binario): b = (b & ~1) | int(binario[i]); i += 1
        nuevos_datos.append((r, g, b))

    nueva = Image.new("RGB", img.size)
    nueva.putdata(nuevos_datos)
    return nueva

def extraer_mensaje_de_imagen(img: Image.Image) -> str:
    """
    Extrae el mensaje oculto de una imagen si está marcado con 'STEG:'.
    """
    datos = list(img.convert('RGB').getdata())
    bits = ''.join([str(c & 1) for pixel in datos for c in pixel])
    bytes_list = [bits[i:i+8] for i in range(0, len(bits), 8)]
    bin_data = bytearray()
    for byte in bytes_list:
        if byte == '00000000': break
        bin_data.append(int(byte, 2))

    mensaje = bin_data.decode('utf-8', errors='replace')

    if mensaje.startswith(MARCADOR):
        return mensaje[len(MARCADOR):]  # Devuelve el mensaje sin el prefijo
    else:
        return ""  # No contiene mensaje válido
