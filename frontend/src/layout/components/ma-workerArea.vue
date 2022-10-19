
<template>
  <a-layout-content class="work-area customer-scrollbar relative">
    <div class="h-full" :class="{ 'p-3': $route.path.indexOf('maIframe') === -1 }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <keep-alive :include="keepStore.keepAlives">
            <component :is="Component" :key="$route.name" v-if="keepStore.show" />
          </keep-alive>
        </transition>
      </router-view>
      <iframe-view />
    </div>
  </a-layout-content>
</template>

<script setup>
  import { useKeepAliveStore } from '@/store'
  import IframeView from './components/iframe-view.vue'
  const keepStore = useKeepAliveStore()
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
