import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart, RadarChart, GaugeChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  GraphicComponent,
} from 'echarts/components'

import MaCrud from './sk-crud/index.vue'
import MaForm from './sk-form/index.vue'
import MaChart from './sk-charts/index.vue'
import MaUpload from './sk-upload/index.vue'
import MaTreeSlider from './sk-treeSlider/index.vue'
import MaResource from './sk-resource/index.vue'
import MaResourceButton from './sk-resource/button.vue'
import MaUser from './sk-user/index.vue'
import MaEditor from './sk-editor/index.vue'
import MaIcon from './sk-icon/index.vue'
import MaCodeEditor from './sk-codeEditor/index.vue'
import MaUserInfo from './sk-userInfo/index.vue'
import MaCityLinkage from './sk-cityLinkage/index.vue'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  RadarChart,
  GaugeChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  GraphicComponent,
]);

export default {
  install(Vue) {
    Vue.component('MaChart', MaChart)
    Vue.component('MaCrud', MaCrud)
    Vue.component('MaForm', MaForm)
    Vue.component('MaUpload', MaUpload)
    Vue.component('MaTreeSlider', MaTreeSlider)
    Vue.component('MaResource', MaResource)
    Vue.component('MaResourceButton', MaResourceButton)
    Vue.component('MaUser', MaUser)
    Vue.component('MaEditor', MaEditor)
    Vue.component('MaIcon', MaIcon)
    Vue.component('MaCodeEditor', MaCodeEditor)
    Vue.component('MaUserInfo', MaUserInfo)
    Vue.component('MaCityLinkage', MaCityLinkage)
  }
}
