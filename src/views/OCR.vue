<template>
  <section class="bg-white p-6 rounded shadow max-w-xl mx-auto relative">
    <!-- Título e icono de ayuda -->
    <div class="flex items-center justify-center gap-2 mb-2">
      <h2 class="text-2xl font-bold text-gray-800 text-center">OCR: Reconocimiento Óptico de Caracteres</h2>
      <div class="group relative">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500 cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M12 2a10 10 0 100 20 10 10 0 000-20z" />
        </svg>
        <div class="absolute w-64 top-7 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-sm p-3 rounded shadow z-10 opacity-0 group-hover:opacity-100 transition-opacity">
          Este OCR detecta texto visible. Si no reconoce nada, prueba con otra imagen que tenga texto claro y legible.
        </div>
      </div>
    </div>

    <p class="text-center text-sm text-gray-600 mb-6">Extrae el texto visible de imágenes como JPG, PNG, GIF...</p>

    <!-- Dropzone -->
    <div
      class="border-2 border-dashed border-blue-400 p-6 rounded text-center mb-4 bg-blue-50 cursor-pointer hover:bg-blue-100"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="$refs.ocrInput.click()"
    >
      <p class="text-sm text-gray-600">Arrastra una imagen aquí o haz clic para seleccionarla</p>
      <input ref="ocrInput" type="file" @change="onImageChange" accept="image/*" class="hidden" />
    </div>

    <!-- Vista previa -->
    <div v-if="preview" class="mb-4 text-center">
      <img :src="preview" alt="Imagen seleccionada" class="max-h-48 mx-auto rounded shadow" />
      <p class="text-sm text-gray-500 mt-2">{{ imagenParaOCR?.name }}</p>
    </div>

    <!-- Botón principal -->
    <button
      @click="realizarOCR"
      :disabled="isLoading || !imagenParaOCR"
      class="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 mb-2 text-base font-medium"
    >
      {{ isLoading ? 'Analizando imagen...' : 'Extraer texto con OCR' }}
    </button>

    <!-- Éxito -->
    <p v-if="ocrExitoso" class="text-green-600 text-center font-medium mb-2">OCR completado con éxito</p>
    <p v-if="idiomaDetectado" class="text-sm text-gray-600 text-center mb-4">Idioma detectado: <strong>{{ idiomaDetectado }}</strong></p>

    <!-- Resultados -->
    <div v-if="resultadoOCR !== null" class="bg-gray-100 p-4 rounded text-gray-800 shadow space-y-4">
      <div>
        <strong class="text-blue-700">Texto detectado:</strong>
        <p class="mt-1 whitespace-pre-line">{{ resultadoOCR || 'No se detectó texto visible.' }}</p>
      </div>

      <div v-if="traduccion">
        <strong class="text-blue-700">Traducción:</strong>
        <p class="mt-1 whitespace-pre-line">{{ traduccion }}</p>
      </div>

      <div class="flex flex-col sm:flex-row gap-4 pt-2">
        <button
          @click="descargarResultados"
          class="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Descargar resultados
        </button>
        <button
          @click="reiniciarFormulario"
          class="flex-1 bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
        >
          Reiniciar
        </button>
      </div>
    </div>

    <!-- Error -->
    <p v-if="error" class="text-red-600 mt-4 text-center">{{ error }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const imagenParaOCR = ref(null)
const preview = ref(null)
const resultadoOCR = ref(null)
const isLoading = ref(false)
const error = ref('')
const ocrExitoso = ref(false)
const idiomaDetectado = ref(null)
const traduccion = ref(null)

function onImageChange(e) {
  const file = e.target.files[0]
  procesarArchivo(file)
}

function handleDrop(e) {
  const file = e.dataTransfer.files[0]
  procesarArchivo(file)
}

function procesarArchivo(file) {
  const permitidos = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/webp', 'image/gif']
  if (!file || !permitidos.includes(file.type)) {
    error.value = 'Selecciona una imagen válida (PNG, JPG, BMP, WEBP, GIF).'
    return
  }

  imagenParaOCR.value = file
  preview.value = URL.createObjectURL(file)
  error.value = ''
  resultadoOCR.value = null
  ocrExitoso.value = false
  idiomaDetectado.value = null
  traduccion.value = null
}

async function realizarOCR() {
  if (!imagenParaOCR.value) return
  isLoading.value = true
  error.value = ''
  resultadoOCR.value = null
  ocrExitoso.value = false
  idiomaDetectado.value = null
  traduccion.value = null

  const form = new FormData()
  form.append('imagen', imagenParaOCR.value)

  try {
    const res = await axios.post('http://localhost:8000/ocr', form)
    resultadoOCR.value = res.data.texto || ''
    idiomaDetectado.value = res.data.idioma || ''
    traduccion.value = res.data.traduccion || ''
    ocrExitoso.value = true

    guardarEnHistorial({
      tipo: 'ocr',
      archivo: imagenParaOCR.value.name,
      timestamp: new Date().toISOString(),
      mensaje: resultadoOCR.value.slice(0, 50)
    })
  } catch (err) {
    console.error(err)
    error.value = 'Error al realizar OCR. Intenta con otra imagen.'
  }

  isLoading.value = false
}

function descargarResultados() {
  let contenido = `Texto detectado:\n${resultadoOCR.value || 'N/A'}\n\nTraducción:\n${traduccion.value || 'N/A'}`
  const blob = new Blob([contenido], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'ocr_resultado.txt'
  a.click()
  URL.revokeObjectURL(url)
}

function reiniciarFormulario() {
  imagenParaOCR.value = null
  preview.value = null
  resultadoOCR.value = null
  isLoading.value = false
  error.value = ''
  ocrExitoso.value = false
  idiomaDetectado.value = null
  traduccion.value = null
}

function guardarEnHistorial(registro) {
  const historial = JSON.parse(localStorage.getItem('historial')) || []
  historial.unshift(registro)
  localStorage.setItem('historial', JSON.stringify(historial))
}
</script>
