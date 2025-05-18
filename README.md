# 🕵️‍♀️ StegaToolkit

**StegaToolkit** es una aplicación web de análisis forense y esteganografía que permite **ocultar y extraer mensajes en imágenes**, realizar **OCR**, analizar **metadatos EXIF**, detectar modificaciones (ELA), dividir por canales RGB y mucho más.  
Ideal para **pentesters**, **investigadores forenses** y entusiastas de la ciberseguridad.

---

## Acceso

https://stegatoolkit.onrender.com

---

## Funcionalidades principales

| Función                  |  Descripción |
|----------------------------|----------------|
| Ocultar texto           | Inserta texto secreto en imágenes PNG/JPG/BMP... |
| Extraer texto oculto    | Detecta y extrae mensajes desde imágenes |
| OCR                     | Extrae texto visible con Tesseract-OCR |
| Historial               | Guarda las acciones del usuario en localStorage |
| Analizador forense      | Revisa metadatos EXIF, hashes MD5/SHA1, RGB y más |
| Análisis ELA            | Detecta manipulaciones en la imagen |
| Split RGB               | Visualiza los canales R, G y B por separado |
| Contacto | Recibo vuestras inquietudes en Telegram |

---

## Tecnologías utilizadas

- **Frontend**: Vue 3, Vite, Tailwind CSS
- **Backend**: FastAPI (Python), Tesseract-OCR, Pillow, Poppler-utils
- **Despliegue**: Render.com (Frontend) y Fly.io (Backend) 
- **Extras**: Docker, .env, API Telegram, localStorage

---

## Modo local para desarrollo

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
npm install
npm run dev
```

Asegúrate de tener `.env` con la variable:

```env
VITE_API_URL=http://localhost:8000
```

---

## Autora

**Beatriz Fresno Naumova**  
[GitHub](https://github.com/beafn28) · [LinkedIn](https://www.linkedin.com/in/beatriz-fresno-naumova-3797b931b) · [GitBook](https://beafn28.gitbook.io/beafn28/) · [HackTheBox](https://app.hackthebox.com/profile/2070042)

---

## Licencia

MIT License — libre uso con atribución.
