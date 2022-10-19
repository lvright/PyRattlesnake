import { createApp } from 'vue'
import ArcoVue from '@arco-design/web-vue'
import ArcoVueIcon from '@arco-design/web-vue/es/icon'

import globalComponents from '@/components'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from '@/i18n'
import directives from './directives'

// 官方样式
// import '@arco-design/web-vue/dist/arco.css'
// MineAdmin样式
import '@arco-themes/vue-mine-admin/index.less'
import './style/skin.less'
import './style/index.css'
import './style/global.less'

import * as maIcons from '@/assets/ma-icons'
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

// 注册ma-icon图标
for (let icon in maIcons) {
  app.component(`MaIcon${icon}`, maIcons[icon])
}

app.config.globalProperties.$tool = tool
app.config.globalProperties.$common = common

app.mount('#app')

tool.capsule('PyRattlesna', `v${packageJson.version} release`)
console.log('PyRattlesna Github https://github.com/lvright/PyRattlesnake')
console.log('芜湖~')