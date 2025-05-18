<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <!-- Navbar -->
<header class="bg-white shadow p-4">
  <div class="flex justify-between items-center">
    <!-- Logo con enlace al inicio -->
    <!-- Logo con enlace al inicio -->
<RouterLink to="/" class="text-2xl font-bold text-black">
  StegaToolkit
</RouterLink>

    <!-- Botón hamburguesa (solo en móviles) -->
    <button @click="mostrarMenu = !mostrarMenu" class="sm:hidden focus:outline-none">
      <svg class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>

    <!-- Menú horizontal (escritorio) -->
<nav class="hidden sm:flex gap-4 text-sm text-black">
  <RouterLink to="/" class="">Inicio</RouterLink>
  <RouterLink to="/ocultar" class="">Ocultar texto</RouterLink>
  <RouterLink to="/extraer" class="">Extraer texto</RouterLink>
  <RouterLink to="/ocr" class="">OCR</RouterLink>
  <RouterLink to="/rgb_split" class="">RGB Split</RouterLink>
  <RouterLink to="/analisis_forense" class="">Análisis Forense</RouterLink>
  <RouterLink to="/historial" class="">Historial</RouterLink>
</nav>
  </div>

  <!-- Menú vertical desplegable (móviles) -->
<nav v-if="mostrarMenu" class="sm:hidden mt-4 flex flex-col gap-2 text-sm text-black">
  <RouterLink @click="cerrarMenu" to="/" class="">Inicio</RouterLink>
  <RouterLink @click="cerrarMenu" to="/ocultar" class="">Ocultar texto</RouterLink>
  <RouterLink @click="cerrarMenu" to="/extraer" class="">Extraer texto</RouterLink>
  <RouterLink @click="cerrarMenu" to="/ocr" class="">OCR</RouterLink>
  <RouterLink @click="cerrarMenu" to="/rgb_split" class="">RGB Split</RouterLink>
  <RouterLink @click="cerrarMenu" to="/analisis_forense" class="">Análisis Forense</RouterLink>
  <RouterLink @click="cerrarMenu" to="/historial" class="">Historial</RouterLink>
</nav>
</header>

    <!-- Contenido dinámico -->
    <main class="flex-1 w-full max-w-5xl mx-auto p-4">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-white text-center text-sm p-4 text-gray-600 border-t">
      Creado por Beatriz Fresno Naumova © 2025
      <div class="mt-2">
<RouterLink to="/privacidad" class="mx-2 underline text-blue-600">Política de privacidad</RouterLink>
<RouterLink to="/contacto" class="mx-2 underline text-blue-600">Contacto</RouterLink>
<RouterLink to="/terminos" class="mx-2 underline text-blue-600">Términos de uso</RouterLink>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const mostrarMenu = ref(false)

function cerrarMenu() {
  mostrarMenu.value = false
}
</script>
