import { createApp } from 'vue'
import ArcoVue from '@arco-design/web-vue'
import ArcoVueIcon from '@arco-design/web-vue/es/icon'

import globalComponents from '@/components'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from '@/i18n'
import directives from './directives'

import '@arco-design/web-vue/dist/arco.css'
import './style/skin.less'
import './style/index.css'
import './style/global.less'

import * as skIcon from '@/assets/sk-icons'
import tool from '@/utils/tool'
import * as common from '@/utils/common'
import packageJson from '../package.json'

const app = createApp(App)

app.use(ArcoVue, {})
.use(ArcoVueIcon)
.use(router)
.use(store)
.use(i18n)
.use(directives)
.use(globalComponents)

// 注册sk-icon图标 --> skIcon
for (let icon in skIcon) {
  app.component(`skIcon${icon}`, skIcon[icon])
}

app.config.globalProperties.$tool = tool
app.config.globalProperties.$common = common

app.mount('#app')

tool.capsule('snake-admin', `v${packageJson.version} release`)
