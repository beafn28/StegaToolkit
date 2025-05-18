import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Ocultar from '../views/Ocultar.vue'
import Extraer from '../views/Extraer.vue'
import OCR from '../views/OCR.vue'
import Historial from '../views/Historial.vue'
import RGB from '../views/RGB.vue'
import AnalisisForense from '../views/AnalisisForense.vue'
import PoliticaPrivacidad from '../views/PoliticaPrivacidad.vue'
import Contacto from '../views/Contacto.vue'
import TerminosUso from '../views/TerminosUso.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/ocultar', name: 'Ocultar', component: Ocultar },
  { path: '/extraer', name: 'Extraer', component: Extraer },
  { path: '/ocr', name: 'OCR', component: OCR },
  { path: '/rgb_split', name: 'RGB', component: RGB },
  { path: '/analisis_forense', name: 'Analisis', component: AnalisisForense },
  { path: '/historial', name: 'Historial', component: Historial },
  { path: '/privacidad', name: 'Privacidad', component: PoliticaPrivacidad },
  { path: '/contacto', name: 'Contacto', component: Contacto },
  { path: '/terminos', name: 'TerminosUso', component: TerminosUso }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
