<template>
  <section class="bg-white p-6 rounded shadow max-w-xl mx-auto">
    <h2 class="text-2xl font-semibold text-gray-800 mb-6 text-center">Extraer texto desde imagen</h2>

    <!-- Zona Drag & Drop -->
    <div
      class="border-2 border-dashed border-blue-400 p-6 rounded text-center mb-4 bg-blue-50 cursor-pointer hover:bg-blue-100"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="$refs.extractInput.click()"
    >
      <p class="text-sm text-gray-600">Arrastra una imagen aquí o haz clic para seleccionarla.</p>
      <input
        ref="extractInput"
        type="file"
        @change="onExtractImageChange"
        accept="image/png,image/jpeg,image/jpg,image/bmp,image/webp,image/gif"
        class="hidden"
      />
    </div>

    <!-- Vista previa -->
    <div v-if="preview" class="mb-4 text-center">
      <img :src="preview" alt="Imagen seleccionada" class="max-h-48 mx-auto rounded shadow" />
      <p class="text-sm text-gray-500 mt-2">{{ imagenParaExtraer?.name }}</p>
    </div>

    <!-- Botones -->
    <div class="flex flex-col sm:flex-row gap-4 mb-4">
      <button
        @click="analizarImagen"
        :disabled="!imagenParaExtraer"
        class="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        Analizar imagen
      </button>
      <button
        @click="extraerTexto"
        :disabled="isLoading || !imagenParaExtraer"
        class="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {{ isLoading ? 'Procesando...' : 'Extraer texto' }}
      </button>
    </div>

    <!-- Resultado del análisis -->
    <div v-if="resultadoAnalisis !== null" class="text-center mb-4">
      <p :class="resultadoAnalisis ? 'text-green-700' : 'text-gray-500'">
        {{ resultadoAnalisis ? 'Se ha detectado un mensaje oculto.' : 'No se detectó texto oculto.' }}
      </p>
    </div>

    <!-- Resultado de extracción -->
    <div v-if="mensajeExtraido !== null" class="mt-4 bg-gray-100 p-4 rounded text-gray-800 shadow">
      <strong class="text-blue-700">Texto extraído:</strong>
      <p class="mt-2 whitespace-pre-line">{{ mensajeExtraido || 'No se detectó texto oculto.' }}</p>

      <button
        v-if="mensajeExtraido"
        @click="descargarTexto"
        class="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Descargar como .txt
      </button>
    </div>

    <!-- Error -->
    <p v-if="error" class="text-red-600 mt-4 text-center">{{ error }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const imagenParaExtraer = ref(null)
const preview = ref(null)
const mensajeExtraido = ref(null)
const resultadoAnalisis = ref(null)
const isLoading = ref(false)
const error = ref('')
const extractInput = ref(null)

function onExtractImageChange(e) {
  const file = e.target.files[0]
  procesarArchivo(file)
}

function handleDrop(e) {
  const file = e.dataTransfer.files[0]
  procesarArchivo(file)
}

function procesarArchivo(file) {
  const formatosPermitidos = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/webp', 'image/gif']
  if (!file || !formatosPermitidos.includes(file.type)) {
    error.value = 'Selecciona una imagen válida (PNG, JPG, BMP, WEBP, GIF).'
    return
  }

  imagenParaExtraer.value = file
  preview.value = URL.createObjectURL(file)
  error.value = ''
  mensajeExtraido.value = null
  resultadoAnalisis.value = null
}

async function analizarImagen() {
  if (!imagenParaExtraer.value) return

  const form = new FormData()
  form.append('imagen', imagenParaExtraer.value)

  try {
    const res = await api.post('/analizar', form)
    resultadoAnalisis.value = res.data.contiene_mensaje
  } catch (err) {
    console.error('Error analizando imagen:', err)
    error.value = 'Error al analizar la imagen.'
    resultadoAnalisis.value = null
  }
}

async function extraerTexto() {
  if (!imagenParaExtraer.value) return
  isLoading.value = true
  error.value = ''
  mensajeExtraido.value = null

  const form = new FormData()
  form.append('imagen', imagenParaExtraer.value)

  try {
    const res = await api.post('/extraer', form)
    mensajeExtraido.value = res.data.mensaje || ''
    guardarEnHistorial({
      tipo: 'extracción',
      archivo: imagenParaExtraer.value.name,
      timestamp: new Date().toISOString(),
      mensaje: mensajeExtraido.value.slice(0, 50)
    })
  } catch (err) {
    console.error(err)
    error.value = 'Error al extraer el texto.'
  }

  isLoading.value = false
}

function descargarTexto() {
  const blob = new Blob([mensajeExtraido.value], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'mensaje_extraido.txt'
  a.click()
  URL.revokeObjectURL(url)
}

function guardarEnHistorial(registro) {
  const historial = JSON.parse(localStorage.getItem('historial')) || []
  historial.unshift(registro)
  localStorage.setItem('historial', JSON.stringify(historial))
}
</script>
