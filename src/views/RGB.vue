<template>
  <section class="bg-white p-6 rounded shadow max-w-xl mx-auto relative">
    <div class="flex items-center justify-center gap-2 mb-2">
      <h2 class="text-2xl font-bold text-gray-800 text-center">RGB Split</h2>
      <div class="group relative">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500 cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M12 2a10 10 0 100 20 10 10 0 000-20z" />
        </svg>
        <div class="absolute w-64 top-7 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-sm p-3 rounded shadow z-10 opacity-0 group-hover:opacity-100 transition-opacity">
          Separa los canales de color R, G y B de una imagen y observa su composición por separado.
        </div>
      </div>
    </div>

    <p class="text-center text-sm text-gray-600 mb-6">
      Arrastra una imagen o selecciónala para ver sus canales RGB.
    </p>

    <!-- Drag & Drop -->
    <div
      class="border-2 border-dashed border-blue-400 p-6 rounded text-center mb-4 bg-blue-50 cursor-pointer hover:bg-blue-100"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="$refs.rgbInput.click()"
    >
      <p class="text-sm text-gray-600">Arrastra una imagen aquí o haz clic para seleccionarla</p>
      <input
        ref="rgbInput"
        type="file"
        @change="onImageChange"
        accept="image/*"
        class="hidden"
      />
    </div>

    <!-- Vista previa original -->
    <div v-if="preview" class="mb-6 text-center">
      <img :src="preview" alt="Imagen original" class="max-h-48 mx-auto rounded shadow" />
      <p class="text-sm text-gray-500 mt-2">{{ archivo?.name }}</p>
    </div>

    <!-- Canales RGB -->
    <div v-if="canales.rojo" class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
      <div class="text-center">
        <p class="text-sm font-semibold text-red-600 mb-1">Canal Rojo</p>
        <img :src="canales.rojo" class="w-full h-auto rounded shadow" />
      </div>
      <div class="text-center">
        <p class="text-sm font-semibold text-green-600 mb-1">Canal Verde</p>
        <img :src="canales.verde" class="w-full h-auto rounded shadow" />
      </div>
      <div class="text-center">
        <p class="text-sm font-semibold text-blue-600 mb-1">Canal Azul</p>
        <img :src="canales.azul" class="w-full h-auto rounded shadow" />
      </div>
    </div>

    <!-- Botones -->
    <div v-if="canales.rojo" class="flex justify-center gap-4">
      <button @click="reiniciar" class="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300">
        Reiniciar
      </button>
      <button @click="descargarTodos" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        Descargar canales
      </button>
    </div>

    <p v-if="error" class="text-red-600 text-center mt-4">{{ error }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const archivo = ref(null)
const preview = ref(null)
const canales = ref({ rojo: null, verde: null, azul: null })
const error = ref('')
const rgbInput = ref(null)

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
  canales.value = { rojo: null, verde: null, azul: null }
  enviarImagen()
}

async function enviarImagen() {
  const formData = new FormData()
  formData.append('imagen', archivo.value)

  try {
    const res = await axios.post('http://localhost:8000/rgb_split', formData)
    canales.value = {
      rojo: 'data:image/png;base64,' + res.data.rojo,
      verde: 'data:image/png;base64,' + res.data.verde,
      azul: 'data:image/png;base64,' + res.data.azul,
    }

    guardarEnHistorial({
      tipo: 'rgb_split',
      archivo: archivo.value.name,
      timestamp: new Date().toISOString(),
      mensaje: 'Canales separados'
    })
  } catch (err) {
    error.value = 'Error al procesar la imagen.'
    console.error(err)
  }
}

function reiniciar() {
  archivo.value = null
  preview.value = null
  canales.value = { rojo: null, verde: null, azul: null }
  rgbInput.value.value = null
}

function descargarTodos() {
  for (const canal in canales.value) {
    const enlace = document.createElement('a')
    enlace.href = canales.value[canal]
    enlace.download = `canal_${canal}.png`
    enlace.click()
  }
}

function guardarEnHistorial(registro) {
  const historial = JSON.parse(localStorage.getItem('historial')) || []
  historial.unshift(registro)
  localStorage.setItem('historial', JSON.stringify(historial))
}
</script>
