
<template>
  <st-welcome />
  <st-count />
  <st-login-chart />

  <div class="block lg:flex">
    <st-announced />
    <st-snakeadmin />
  </div>
</template>

<script setup>
  import StCount from './components/st-count.vue'
  import StWelcome from './components/st-welcome.vue'
  import StLoginChart from './components/st-loginChart.vue'
  import StSnakeAdmin from './components/st-snakeadmin.vue'
  import StAnnounced from './components/st-announced.vue'
</script>

