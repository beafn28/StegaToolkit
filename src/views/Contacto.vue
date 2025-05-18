<template>
  <div class="max-w-3xl mx-auto p-8 bg-white rounded shadow text-gray-800">
    <h1 class="text-3xl font-bold mb-4">Contacto</h1>
    <p class="mb-6">¿Tienes dudas, sugerencias o ideas para <strong>StegaToolkit</strong>? Escríbeme:</p>

    <form @submit.prevent="enviarMensaje" class="space-y-4">
      <div>
        <label class="block text-sm font-medium">Nombre</label>
        <input type="text" v-model="nombre" required class="w-full p-2 border rounded" />
      </div>

      <div>
        <label class="block text-sm font-medium">Correo</label>
        <input type="email" v-model="correo" required class="w-full p-2 border rounded" />
      </div>

      <div>
        <label class="block text-sm font-medium">Mensaje</label>
        <textarea v-model="mensaje" required class="w-full p-2 border rounded" rows="5"></textarea>
      </div>

      <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700" :disabled="enviando">
        {{ enviando ? 'Enviando...' : 'Enviar mensaje' }}
      </button>

      <p v-if="confirmacion" class="text-green-600 mt-2">{{ confirmacion }}</p>
      <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const nombre = ref('')
const correo = ref('')
const mensaje = ref('')
const enviando = ref(false)
const confirmacion = ref('')
const error = ref('')

async function enviarMensaje() {
  enviando.value = true
  confirmacion.value = ''
  error.value = ''

  const form = new FormData()
  form.append('nombre', nombre.value)
  form.append('correo', correo.value)
  form.append('mensaje', mensaje.value)

  try {
    const res = await axios.post('http://localhost:8000/contacto', form)
    confirmacion.value = res.data.message
    nombre.value = ''
    correo.value = ''
    mensaje.value = ''
  } catch (e) {
    error.value = 'Hubo un problema al enviar el mensaje.'
  }

  enviando.value = false
}
</script>
