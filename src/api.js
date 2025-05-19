import axios from 'axios'

const baseURL = import.meta.env.DEV ? '/api' : 'https://backend-falling-breeze-4140.fly.dev'

const api = axios.create({
  baseURL
})

export default api