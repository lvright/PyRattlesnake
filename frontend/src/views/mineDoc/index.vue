
<template>
  <div class="h-full">
    <doc-main v-if="docStore.auth" />
    <auth v-else  />
  </div>
</template>

<script setup>
import { useDocStore } from '@/store'
import Auth from './components/auth.vue'
import DocMain from './components/docMain.vue'

const docStore = useDocStore()
</script>
