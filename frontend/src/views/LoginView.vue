<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import AuthForm from '@/components/AuthForm.vue';
import api from '@/services/api.js';
import auth from '@/store/auth.js'; //

const router = useRouter();
const error = ref(null);

const handleLogin = async (formData) => {
  error.value = null;
  try {
    const response = await api.loginUser(formData);
    auth.login(response.data.access);
    router.push('/');
  } catch (e) {
    console.error('Login error:', e.response.data);
    error.value = 'Incorrect username or password.';
  }
};
</script>

<template>
  <div>
    <AuthForm formType="login" :submitForm="handleLogin" />
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<style scoped>
.error-message {
  color: red;
  text-align: center;
  margin-top: 1rem;
}
</style>
