<script setup>
  import { reactive, ref, onMounted } from 'vue'
  import verifyCode from '@cps/ma-verifyCode/index.vue'
  import { Message } from '@arco-design/web-vue'
  import { useUserStore } from '@/store'
  import { useRouter, useRoute } from 'vue-router'

  const router = useRouter()
  const route  = useRoute()

  const Verify = ref(null)

  const loading = ref(false)
  const form = reactive({ username: 'superAdmin', password: '888888', code: '' })

  const userStore = useUserStore()

  const redirect = route.query.redirect ? route.query.redirect : '/'

  const handleSubmit = async ({ values, errors }) => {
    if (loading.value) {
      return
    }
    loading.value = true
    if (Verify.value.checkResult(form.code) && (! errors)) {
      let formData = new FormData()
      formData.append("username", form.username)
      formData.append("password", form.password)
      const result = await userStore.login(formData)
      if (! result) {
        loading.value = false
        return
      }
      router.push(redirect)
    }
    loading.value = false
  }
</script>
<template>
  <div class="login-container">
    <div class="login-width mx-auto flex justify-between h-full items-center">
      <div class="md:w-6/12 w-11/12 md:rounded-r md:rounded-l mx-auto pl-5 pr-5 pb-10 bg-white">
        <div class="logo mx-auto flex justify-between h-full items-center">
          <img src="/logo-w.svg" width="280">
        </div>
        <h2 class="mt-10 text-3xl pb-0 mb-10">{{ $t('sys.login.title') }}</h2>
        <a-form :model="form" @submit="handleSubmit">
          <a-form-item
            field="username"
            :hide-label="true"
            :rules="[{ required: true, message: $t('sys.login.usernameNotice') }]"
          >
            <a-input
              v-model="form.username"
              class="w-full"
              size="large"
              :placeholder="$t('sys.login.username')"
              allow-clear
            >
              <template #prefix><icon-user /></template>
            </a-input>
          </a-form-item>

          <a-form-item
            field="password"
            :hide-label="true"
            :rules="[{ required: true, message: $t('sys.login.passwordNotice') }]"
          >
            <a-input-password
              v-model="form.password"
              :placeholder="$t('sys.login.password')"
              size="large"
              allow-clear
            >
              <template #prefix><icon-lock /></template>
            </a-input-password>
          </a-form-item>

          <a-form-item
            field="code"
            :hide-label="true"
            :rules="[{
              required: true,
              match: /^[a-zA-Z0-9]{4}$/,
              message: $t('sys.login.verifyCodeNotice')
            }]"
          >
            <a-input
              v-model="form.code"
              :placeholder="$t('sys.login.verifyCode')"
              size="large"
              allow-clear
            >
              <template #prefix><icon-safe /></template>
              <template #append>
                <verify-code ref="Verify" />
              </template>
            </a-input>
          </a-form-item>

          <a-form-item :hide-label="true" class="mt-5">
            <a-button html-type="submit" type="primary" long size="large" :loading="loading">
              {{ $t('sys.login.loginBtn') }}
            </a-button>
          </a-form-item>

        </a-form>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.login-container {
  width: 100%;
  height: 100%;
  position: absolute;
  background-image: url(https://api.dujin.org/bing/1920.php);
  background-size: cover;

  .login-width {
    max-width: 860px;
    min-width: 400px;
  }

  .logo {
    width: 260px;
    display: flex; 
    margin-top: 20px; 
    color: #333;
  }
  :deep(.arco-input-append) {
    padding: 0 !important;
  }
  .qq:hover, .alipay:hover {
    background: #5770F5;
  }
  .wechat:hover {
    background: #0f9c02;
  }
  .weibo:hover {
    background: #f3ce2b;
  }
}
</style>