
<template>
  <a-layout class="layout flex justify-between h-full">

    <ma-classic-sider />

    <a-layout-content class="flex flex-col">
      <ma-classic-header />
      <ma-worker-area />
    </a-layout-content>

  </a-layout>
</template>

<script setup>
import { ref } from 'vue'

import MaClassicSider from './ma-classic-sider.vue'
import MaClassicHeader from './ma-classic-header.vue'
import MaWorkerArea from '../ma-workerArea.vue'

</script>
