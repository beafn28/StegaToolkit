<template>
  <section class="bg-white p-6 rounded shadow max-w-2xl mx-auto relative">
    <div class="flex items-center justify-center gap-2 mb-2">
      <h2 class="text-2xl font-bold text-gray-800 text-center">Análisis Forense de Imagen</h2>
      <div class="group relative">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500 cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M12 2a10 10 0 100 20 10 10 0 000-20z" />
        </svg>
        <div class="absolute w-64 top-7 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-sm p-3 rounded shadow z-10 opacity-0 group-hover:opacity-100 transition-opacity">
          Este análisis extrae metadatos, hashes, detecta texto oculto y mostrará alteraciones ELA.
        </div>
      </div>
    </div>

    <p class="text-center text-sm text-gray-600 mb-6">
      Sube una imagen para inspeccionarla digitalmente.
    </p>

    <!-- Drag & Drop -->
    <div
      class="border-2 border-dashed border-blue-400 p-6 rounded text-center mb-4 bg-blue-50 cursor-pointer hover:bg-blue-100"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="$refs.analisisInput.click()"
    >
      <p class="text-sm text-gray-600">Arrastra una imagen aquí o haz clic para seleccionarla</p>
      <input
        ref="analisisInput"
        type="file"
        @change="onImageChange"
        accept="image/*"
        class="hidden"
      />
    </div>

    <!-- Vista previa -->
    <div v-if="preview" class="mb-4 text-center">
      <img :src="preview" alt="Imagen seleccionada" class="max-h-48 mx-auto rounded shadow" />
      <p class="text-sm text-gray-500 mt-2">{{ archivo?.name }}</p>
    </div>

    <!-- Botón analizar -->
    <button
      @click="analizarImagen"
      :disabled="isLoading || !archivo"
      class="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 mb-4 text-base font-medium"
    >
      {{ isLoading ? 'Analizando...' : 'Analizar imagen' }}
    </button>

    <!-- Resultados -->
    <div v-if="resultado" class="space-y-6">
      <!-- Metadatos -->
      <div class="bg-gray-100 p-4 rounded shadow">
        <strong class="text-blue-700">Metadatos EXIF:</strong>
        <ul class="mt-2 text-sm text-gray-700 list-disc list-inside">
          <li v-for="(v, k) in resultado.exif" :key="k"><strong>{{ k }}:</strong> {{ v }}</li>
        </ul>
        <p v-if="Object.keys(resultado.exif).length === 0" class="text-gray-500 italic mt-2">Sin metadatos.</p>
      </div>

      <!-- Hashes -->
      <div class="bg-gray-100 p-4 rounded shadow">
        <strong class="text-blue-700">🔍 Hashes:</strong>
        <p class="mt-2 text-sm text-gray-800">MD5: {{ resultado.md5 }}</p>
        <p class="text-sm text-gray-800">SHA1: {{ resultado.sha1 }}</p>
      </div>

      <!-- Mensaje oculto -->
      <div class="bg-gray-100 p-4 rounded shadow">
        <strong class="text-blue-700">¿Contiene texto oculto?</strong>
        <p class="mt-2 text-gray-800">
          {{ resultado.contiene_mensaje ? 'Sí, contiene mensaje oculto.' : 'No se detectó mensaje oculto.' }}
        </p>
      </div>

      <!-- ELA -->
      <div v-if="elaBase64" class="bg-gray-100 p-4 rounded shadow">
        <strong class="text-blue-700">ELA (Error Level Analysis):</strong>
        <p class="text-sm text-gray-600 mt-2">Áreas más brillantes pueden indicar alteraciones digitales.</p>
        <img :src="'data:image/png;base64,' + elaBase64" alt="ELA" class="mt-3 rounded shadow max-w-full" />
      </div>

<!-- Botones ELA + Reinicio -->
<div class="flex justify-center gap-4 mt-4">
  <button @click="obtenerELA" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
    Mostrar análisis ELA
  </button>
  <button @click="reiniciar" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
    Reiniciar análisis
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

const archivo = ref(null)
const preview = ref(null)
const analisisInput = ref(null)
const isLoading = ref(false)
const resultado = ref(null)
const error = ref('')
const elaBase64 = ref(null)

function handleDrop(e) {
  const file = e.dataTransfer.files[0]
  procesarArchivo(file)
}

function onImageChange(e) {
  const file = e.target.files[0]
  procesarArchivo(file)
}

function procesarArchivo(file) {
  if (!file || !file.type.startsWith('image/')) {
    error.value = 'Selecciona una imagen válida.'
    return
  }
  archivo.value = file
  preview.value = URL.createObjectURL(file)
  error.value = ''
  resultado.value = null
  elaBase64.value = null
}

async function analizarImagen() {
  if (!archivo.value) return
  isLoading.value = true
  error.value = ''
  resultado.value = null
  elaBase64.value = null

  const formData = new FormData()
  formData.append('imagen', archivo.value)

  try {
    const res = await axios.post('http://localhost:8000/analisis_forense', formData)
    resultado.value = res.data
    guardarEnHistorial({
      tipo: 'analisis_forense',
      archivo: archivo.value.name,
      timestamp: new Date().toISOString(),
      mensaje: resultado.value.contiene_mensaje ? 'Contiene mensaje oculto' : 'No contiene mensaje'
    })
  } catch (err) {
    error.value = 'Error al analizar la imagen.'
    console.error(err)
  }

  isLoading.value = false
}

async function obtenerELA() {
  const formData = new FormData()
  formData.append('imagen', archivo.value)

  try {
    const res = await axios.post('http://localhost:8000/ela', formData)
    elaBase64.value = res.data.ela
  } catch (err) {
    error.value = 'Error obteniendo ELA.'
    console.error(err)
  }
}

function reiniciar() {
  archivo.value = null
  preview.value = null
  resultado.value = null
  elaBase64.value = null
  analisisInput.value.value = null
  error.value = ''
}

function guardarEnHistorial(registro) {
  const historial = JSON.parse(localStorage.getItem('historial')) || []
  historial.unshift(registro)
  localStorage.setItem('historial', JSON.stringify(historial))
}
</script>
