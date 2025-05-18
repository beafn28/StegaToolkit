<template>
  <section class="bg-white p-10 rounded shadow text-center">
    <h1 class="text-4xl font-bold text-gray-800 mb-4">Bienvenid@ a StegaToolkit</h1>
    <p class="text-lg text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed text-justify">
      Una herramienta avanzada para ocultar, analizar y extraer mensajes en imágenes usando esteganografía moderna.
    </p>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
      <RouterLink
        to="/ocultar"
        class="flex flex-col items-center justify-center p-6 rounded-lg shadow hover:shadow-lg transition bg-blue-100 hover:bg-blue-200 text-justify"
      >
        <h2 class="text-lg font-semibold text-blue-700 mb-2 text-center">Ocultar texto</h2>
        <p class="text-sm text-gray-700">Inserta un mensaje secreto en una imagen PNG sin modificar su apariencia.</p>
      </RouterLink>

      <RouterLink
        to="/extraer"
        class="flex flex-col items-center justify-center p-6 rounded-lg shadow hover:shadow-lg transition bg-blue-100 hover:bg-blue-200 text-justify"
      >
        <h2 class="text-lg font-semibold text-blue-700 mb-2 text-center">Extraer texto</h2>
        <p class="text-sm text-gray-700">Recupera mensajes previamente ocultos desde imágenes compatibles.</p>
      </RouterLink>

      <RouterLink
        to="/ocr"
        class="flex flex-col items-center justify-center p-6 rounded-lg shadow hover:shadow-lg transition bg-blue-100 hover:bg-blue-200 text-justify"
      >
        <h2 class="text-lg font-semibold text-blue-700 mb-2 text-center">OCR</h2>
        <p class="text-sm text-gray-700">Detecta y extrae texto visible desde imágenes mediante reconocimiento óptico.</p>
      </RouterLink>

      <RouterLink
        to="/rgb_split"
        class="flex flex-col items-center justify-center p-6 rounded-lg shadow hover:shadow-lg transition bg-blue-100 hover:bg-blue-200 text-justify"
      >
        <h2 class="text-lg font-semibold text-blue-700 mb-2 text-center">Análisis RGB</h2>
        <p class="text-sm text-gray-700">Visualiza cada canal de color (R, G, B) por separado para detectar patrones ocultos.</p>
      </RouterLink>

<RouterLink
  to="/analisis-forense"
  class="flex flex-col items-center justify-center p-6 rounded-lg shadow hover:shadow-lg transition bg-blue-100 hover:bg-blue-200 text-justify"
>
  <h2 class="text-lg font-semibold text-blue-700 mb-2 text-center">Análisis Forense</h2>
  <p class="text-sm text-gray-700">Analiza metadatos, hashes, texto oculto y alteraciones digitales en imágenes.</p>
</RouterLink>

      <RouterLink
        to="/historial"
        class="flex flex-col items-center justify-center p-6 rounded-lg shadow hover:shadow-lg transition bg-blue-100 hover:bg-blue-200 text-justify"
      >
        <h2 class="text-lg font-semibold text-blue-700 mb-2 text-center">Historial</h2>
        <p class="text-sm text-gray-700">Revisa el registro de acciones realizadas en esta sesión.</p>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
