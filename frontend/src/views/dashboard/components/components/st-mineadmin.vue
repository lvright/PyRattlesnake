
<template>
  <div class="w-full lg:w-3/12 ma-content-block rounded-sm ml-0 lg:ml-3 p-3 mt-3">
    <div class="flex">
      PyRattlesnake 相关
    </div>
    <div class="w-11/12 mx-auto mt-3">
      <a-tag class="ml-0.5">PyRattlesnake v{{ config.version }} release</a-tag>
    </div>
  </div>
</template>

<script setup>
  import config from '@/../package.json'

  const openPage = (url = '') => {
    window.open(url)
  }
</script>