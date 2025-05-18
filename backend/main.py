from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from stega_utils import ocultar_mensaje_en_imagen, extraer_mensaje_de_imagen
from io import BytesIO
from PIL import Image, ExifTags
from dotenv import load_dotenv
import os
import requests
import datetime
from pytesseract import image_to_string
from langdetect import detect
from deep_translator import GoogleTranslator
import easyocr
import numpy as np
from base64 import b64encode
import hashlib
import json
from pathlib import Path

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

HISTORIAL = []
HISTORIAL_PATH = Path("historial.json")

def cargar_historial():
    global HISTORIAL
    if HISTORIAL_PATH.exists():
        with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
            try:
                HISTORIAL = json.load(f)
            except json.JSONDecodeError:
                HISTORIAL = []

def guardar_historial():
    with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
        json.dump(HISTORIAL, f, indent=2, ensure_ascii=False)

def registrar_evento(tipo, nombre_archivo, mensaje=None):
    HISTORIAL.append({
        "tipo": tipo,
        "archivo": nombre_archivo,
        "timestamp": datetime.datetime.now().isoformat(),
        "mensaje": mensaje[:50] + "..." if mensaje else None
    })
    guardar_historial()

cargar_historial()

@app.post("/ocultar")
async def ocultar(imagen: UploadFile = File(...), mensaje: str = Form(...)):
    if imagen.content_type.split("/")[0] != "image":
        return JSONResponse(status_code=400, content={"error": "Archivo no válido, debe ser una imagen."})

    contenido = await imagen.read()
    try:
        img = Image.open(BytesIO(contenido)).convert("RGB")
        img_oculta = ocultar_mensaje_en_imagen(img, mensaje)
        buffer = BytesIO()
        img_oculta.save(buffer, format="PNG")
        buffer.seek(0)

        registrar_evento("ocultación", imagen.filename, mensaje)

        return StreamingResponse(buffer, media_type="image/png")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error procesando imagen: {str(e)}"})

@app.post("/extraer")
async def extraer(imagen: UploadFile = File(...)):
    if imagen.content_type.split("/")[0] != "image":
        return JSONResponse(status_code=400, content={"error": "Archivo no válido, debe ser una imagen."})

    contenido = await imagen.read()
    try:
        img = Image.open(BytesIO(contenido)).convert("RGB")
        mensaje = extraer_mensaje_de_imagen(img)

        registrar_evento("extracción", imagen.filename, mensaje)

        return {"mensaje": mensaje}
    except Exception:
        return JSONResponse(status_code=500, content={"error": "Error extrayendo mensaje de la imagen."})

@app.post("/analizar")
async def analizar(imagen: UploadFile = File(...)):
    if imagen.content_type.split("/")[0] != "image":
        return JSONResponse(status_code=400, content={"error": "Archivo no válido, debe ser una imagen."})

    try:
        contenido = await imagen.read()
        img = Image.open(BytesIO(contenido)).convert("RGB")
        mensaje = extraer_mensaje_de_imagen(img)
        return {"contiene_mensaje": mensaje.strip().startswith("STEG:")}
    except Exception:
        return JSONResponse(status_code=500, content={"error": "Error al analizar la imagen."})

@app.post("/contacto")
async def contacto(nombre: str = Form(...), correo: str = Form(...), mensaje: str = Form(...)):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return JSONResponse(status_code=500, content={"error": "Configuración de Telegram no disponible"})

    texto = f"📬 Nuevo mensaje desde StegaToolkit:\n👤 Nombre: {nombre}\n📧 Correo: {correo}\n📝 Mensaje:\n{mensaje}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        requests.post(url, data={"chat_id": chat_id, "text": texto})
        return {"success": True, "message": "Mensaje enviado correctamente"}
    except Exception:
        return JSONResponse(status_code=500, content={"error": "Error enviando a Telegram"})

@app.get("/historial")
def historial():
    return HISTORIAL

@app.post("/ocr")
async def ocr(imagen: UploadFile = File(...)):
    if imagen.content_type.split("/")[0] != "image":
        return JSONResponse(status_code=400, content={"error": "Archivo no válido, debe ser una imagen."})

    try:
        contenido = await imagen.read()
        img = Image.open(BytesIO(contenido)).convert("RGB")
        np_img = np.array(img)

        reader = easyocr.Reader(['es', 'en'], gpu=False)
        resultados = reader.readtext(np_img, detail=0)

        texto = " ".join(resultados).strip()

        if not texto:
            return JSONResponse(status_code=200, content={"texto": "", "idioma": "", "traduccion": ""})

        idioma = detect(texto)
        idioma_nombre = {"es": "Español", "en": "Inglés"}.get(idioma, idioma)

        traduccion = GoogleTranslator(source='auto', target='es' if idioma != 'es' else 'en').translate(texto)

        registrar_evento("ocr", imagen.filename, texto)

        return {
            "texto": texto,
            "idioma": idioma_nombre,
            "traduccion": traduccion
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error realizando OCR: {str(e)}"})

@app.post("/rgb_split")
async def rgb_split(imagen: UploadFile = File(...)):
    if imagen.content_type.split("/")[0] != "image":
        return JSONResponse(status_code=400, content={"error": "Debe ser una imagen."})

    try:
        contenido = await imagen.read()
        img = Image.open(BytesIO(contenido)).convert("RGB")
        r, g, b = img.split()

        def canal_to_base64(canal):
            img_canal = Image.merge("RGB", (
                canal if canal == r else Image.new("L", canal.size),
                canal if canal == g else Image.new("L", canal.size),
                canal if canal == b else Image.new("L", canal.size),
            ))
            buffer = BytesIO()
            img_canal.save(buffer, format="PNG")
            return b64encode(buffer.getvalue()).decode()

        registrar_evento("rgb_split", imagen.filename)

        return {
            "rojo": canal_to_base64(r),
            "verde": canal_to_base64(g),
            "azul": canal_to_base64(b),
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error en RGB Split: {str(e)}"})

@app.post("/analisis_forense")
async def analisis_forense(imagen: UploadFile = File(...)):
    if imagen.content_type.split("/")[0] != "image":
        return JSONResponse(status_code=400, content={"error": "Debe ser una imagen."})

    try:
        contenido = await imagen.read()
        buffer = BytesIO(contenido)
        img = Image.open(buffer)
        exif = {}
        if hasattr(img, '_getexif') and img._getexif():
            exif_raw = img._getexif()
            exif = {
                ExifTags.TAGS.get(k, str(k)): str(v)
                for k, v in exif_raw.items() if k in ExifTags.TAGS
            }

        md5 = hashlib.md5(contenido).hexdigest()
        sha1 = hashlib.sha1(contenido).hexdigest()

        img_rgb = img.convert("RGB")
        mensaje = extraer_mensaje_de_imagen(img_rgb)

        registrar_evento("analisis_forense", imagen.filename, mensaje)

        return {
            "exif": exif,
            "md5": md5,
            "sha1": sha1,
            "contiene_mensaje": bool(mensaje.strip())
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error en análisis forense: {str(e)}"})

@app.post("/ela")
async def ela(imagen: UploadFile = File(...)):
    try:
        contenido = await imagen.read()
        original = Image.open(BytesIO(contenido)).convert("RGB")
        buffer = BytesIO()
        original.save(buffer, format="JPEG", quality=90)
        buffer.seek(0)
        recompressed = Image.open(buffer)

        ela_img = Image.new("RGB", original.size)
        for x in range(original.width):
            for y in range(original.height):
                orig_px = np.array(original.getpixel((x, y)))
                rec_px = np.array(recompressed.getpixel((x, y)))
                diff = tuple(np.clip(abs(orig_px - rec_px) * 10, 0, 255))
                ela_img.putpixel((x, y), tuple(map(int, diff)))

        final_buffer = BytesIO()
        ela_img.save(final_buffer, format="PNG")
        return {"ela": b64encode(final_buffer.getvalue()).decode()}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error generando ELA: {str(e)}"})
