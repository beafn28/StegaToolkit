<template>
  <section class="bg-white p-6 rounded shadow max-w-xl mx-auto">
    <h2 class="text-2xl font-semibold text-gray-800 mb-6 text-center">Ocultar texto en imagen</h2>

    <!-- Zona Drag & Drop -->
    <div
      class="border-2 border-dashed border-blue-400 p-6 rounded text-center mb-4 bg-blue-50 cursor-pointer hover:bg-blue-100"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="$refs.fileInput.click()"
    >
      <p class="text-sm text-gray-600">Arrastra una imagen aquí o haz clic para seleccionarla.</p>
      <input
        ref="fileInput"
        type="file"
        @change="onImageChange"
        accept="image/png,image/jpeg,image/jpg,image/bmp,image/webp,image/gif"
        class="hidden"
      />
    </div>

    <!-- Vista previa -->
    <div v-if="preview" class="mb-4 text-center">
      <img :src="preview" alt="Imagen seleccionada" class="max-h-48 mx-auto rounded shadow" />
      <p class="text-sm text-gray-500 mt-2">{{ imagenOriginal?.name }}</p>
      <p class="text-sm text-gray-500">Capacidad: hasta {{ capacidadMaxima }} caracteres ocultables</p>
    </div>

    <!-- Mensaje secreto -->
    <label class="block text-sm font-medium mb-1 text-gray-700">Mensaje secreto:</label>
    <textarea
      v-model="mensaje"
      placeholder="Escribe aquí tu mensaje oculto (texto, emojis, tildes...)"
      class="w-full p-2 border rounded mb-1"
      rows="4"
    ></textarea>
    <p class="text-xs text-gray-500 text-right mb-4">
      {{ mensaje.length }} / {{ capacidadMaxima }} caracteres
    </p>

    <!-- Botones -->
    <div class="flex flex-col sm:flex-row gap-4 mb-4">
      <button
        @click="ocultarTexto"
        :disabled="isLoading || !imagenOriginal || !mensaje"
        class="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {{ isLoading ? 'Procesando...' : 'Ocultar mensaje' }}
      </button>
      <button
        @click="reiniciar"
        class="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Reiniciar
      </button>
    </div>

    <!-- Analizador -->
    <div class="mb-6">
      <button
        @click="analizarImagen"
        :disabled="!imagenOriginal"
        class="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        Analizar imagen
      </button>
      <div v-if="resultadoAnalisis !== null" class="mt-4 text-center">
        <p :class="resultadoAnalisis ? 'text-green-700' : 'text-gray-500'">
          {{ resultadoAnalisis ? 'Se ha detectado un mensaje oculto en la imagen.' : 'No se detectó mensaje oculto.' }}
        </p>
      </div>
    </div>

    <!-- Resultado -->
    <div v-if="imagenOculta" class="mt-6 text-center">
      <p class="text-green-700 font-semibold">Mensaje ocultado correctamente.</p>
      <a
        :href="imagenOculta"
        download="imagen_con_texto.png"
        class="inline-block mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Descargar imagen
      </a>
    </div>

    <!-- Error -->
    <p v-if="error" class="text-red-600 mt-4 text-center">{{ error }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const imagenOriginal = ref(null)
const preview = ref(null)
const imagenOculta = ref(null)
const mensaje = ref('')
const isLoading = ref(false)
const error = ref('')
const capacidadMaxima = ref(0)
const resultadoAnalisis = ref(null)
const fileInput = ref(null)

function onImageChange(e) {
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

  imagenOriginal.value = file
  preview.value = URL.createObjectURL(file)
  calcularCapacidad(file)
  error.value = ''
  resultadoAnalisis.value = null
}

function calcularCapacidad(file) {
  const img = new Image()
  img.onload = () => {
    const capacidad = Math.floor((img.width * img.height * 3) / 8)
    capacidadMaxima.value = capacidad
  }
  img.src = URL.createObjectURL(file)
}

async function ocultarTexto() {
  if (!imagenOriginal.value || !mensaje.value) return

  if (mensaje.value.length > capacidadMaxima.value) {
    error.value = `El mensaje es demasiado largo. Máximo permitido: ${capacidadMaxima.value} caracteres.`
    return
  }

  isLoading.value = true
  error.value = ''
  imagenOculta.value = null

  const form = new FormData()
  form.append('imagen', imagenOriginal.value)
  form.append('mensaje', mensaje.value)

  try {
    const res = await api.post('/ocultar', form, { responseType: 'blob' })
    imagenOculta.value = URL.createObjectURL(res.data)

    const fecha = new Date().toISOString()
    const resumen = mensaje.value.slice(0, 50)
    guardarEnHistorial({
      tipo: 'ocultación',
      archivo: imagenOriginal.value.name,
      timestamp: fecha,
      mensaje: resumen
    })

    mensaje.value = ''
    imagenOriginal.value = null
    preview.value = null
    capacidadMaxima.value = 0
  } catch (err) {
    console.error(err)
    error.value = 'Error al ocultar el mensaje. Intenta con otra imagen válida.'
  } finally {
    isLoading.value = false
  }
}

async function analizarImagen() {
  if (!imagenOriginal.value) return

  const form = new FormData()
  form.append('imagen', imagenOriginal.value)

  try {
    const res = await api.post('/analizar', form)
    resultadoAnalisis.value = res.data.contiene_mensaje
  } catch (err) {
    console.error('Error analizando imagen:', err)
    error.value = 'No se pudo analizar la imagen.'
    resultadoAnalisis.value = null
  }
}

function reiniciar() {
  imagenOriginal.value = null
  preview.value = null
  mensaje.value = ''
  imagenOculta.value = null
  capacidadMaxima.value = 0
  error.value = ''
  resultadoAnalisis.value = null
}

function guardarEnHistorial(registro) {
  const historial = JSON.parse(localStorage.getItem('historial')) || []
  historial.unshift(registro)
  localStorage.setItem('historial', JSON.stringify(historial))
}
</script>
