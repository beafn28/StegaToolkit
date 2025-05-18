<template>
  <section class="max-w-4xl mx-auto p-6 bg-white rounded shadow text-gray-800">
    <!-- Título -->
    <div class="text-center mb-6">
      <h1 class="text-3xl font-bold text-black">Historial de acciones</h1>
    </div>

    <!-- Mensaje si no hay historial -->
    <div v-if="registros.length === 0" class="text-gray-500 text-center">
      No hay historial todavía.
    </div>

    <!-- Lista de historial -->
    <ul v-else class="grid gap-4">
      <li
        v-for="(registro, index) in registros"
        :key="index"
        class="p-4 bg-blue-50 border border-blue-200 rounded-lg shadow-sm"
      >
        <div class="grid sm:grid-cols-2 gap-2">
          <p><span class="font-semibold">Tipo:</span> {{ registro.tipo }}</p>
          <p><span class="font-semibold">Archivo:</span> {{ registro.archivo }}</p>
          <p><span class="font-semibold">Fecha:</span> {{ formatFecha(registro.timestamp) }}</p>
          <p v-if="registro.mensaje">
            <span class="font-semibold">Mensaje:</span> {{ resumenMensaje(registro.mensaje) }}
          </p>
        </div>
      </li>
    </ul>

    <!-- Botón en la esquina inferior derecha -->
    <div class="flex justify-end mt-6">
      <button
        @click="borrarHistorial"
        class="bg-red-600 text-white p-3 rounded-full hover:bg-red-700 transition"
        title="Borrar historial"
      >
        <!-- Icono de papelera -->
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24"
          stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3m5 0H6" />
        </svg>
      </button>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const registros = ref([])

onMounted(() => {
  const historial = localStorage.getItem('historial')
  registros.value = historial ? JSON.parse(historial).reverse() : []
})

function formatFecha(iso) {
  return new Date(iso).toLocaleString()
}

function resumenMensaje(msg) {
  return msg.length > 50 ? msg.substring(0, 50) + '...' : msg
}

function borrarHistorial() {
  if (confirm('¿Estás segur@ de que quieres borrar todo el historial?')) {
    localStorage.removeItem('historial')
    registros.value = []
  }
}
</script>
