import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import 'animate.css'
import i18n from './i18n'

// define backend API server path for axios
// process.env is already built in by VUE. Simply create and define .env file in root dir
//  for VUE JS env vars, need to have `VUE_APP` prepended
//  to variable name


// first check if we are in DEV_MODE for http
if (process.env.VUE_APP_DEV_MODE === 'false') {
    // if not, check if we are in https mode simulating production environment
    if (process.env.VUE_APP_HTTPS_DEV_MODE === 'true') {
        axios.defaults.baseURL = (process.env.VUE_APP_PRODUCTION_SIM_HTTPS_BACKEND_URL)
    }
    // else we are live
    else {
        axios.defaults.baseURL = (process.env.VUE_APP_PRODUCTION_BACKEND_URL)

    }
}
// else in http mode to use npm's and django's built-in dev server
else {
    axios.defaults.baseURL = (process.env.VUE_APP_HTTP_BACKEND_URL)
}

createApp(App).use(store).use(router, axios).use(i18n).mount('#app')