<template>
  <iframe :src="url" frameborder="0" width="100%" class="frame"></iframe>
</template>

<script setup>
import { ref } from 'vue'
const url = ref(process.env.VUE_APP_URL + '/api/docs')
</script>

<style scoped>
.frame {
  height: calc(100% - 3px)
}
</style>