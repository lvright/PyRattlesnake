<template>
  <a-layout-content class="h-full main-container">
    <columns-layout v-if="appStore.layout === 'columns'" />
    <classic-layout v-if="appStore.layout === 'classic'" />
    <banner-layout v-if="appStore.layout === 'banner'" />

    <ma-button-menu />
  </a-layout-content>
</template>
<script setup>
  import { useAppStore, useUserStore } from '@/store'

  import ColumnsLayout from './components/columns/index.vue'
  import ClassicLayout from './components/classic/index.vue'
  import BannerLayout from './components/banner/index.vue'
  import MaButtonMenu from './components/sk-buttonMenu.vue'

  const appStore = useAppStore()
  const userStore = useUserStore()


</script>
<style scoped lang="less">
</style>
