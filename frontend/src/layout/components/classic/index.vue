
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

import MaClassicSider from './sk-classic-sider.vue'
import MaClassicHeader from './sk-classic-header.vue'
import MaWorkerArea from '../sk-workerArea.vue'

</script>
