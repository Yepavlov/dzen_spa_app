<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import AuthForm from '@/components/AuthForm.vue';
import api from '@/services/api.js';

const router = useRouter();
const error = ref(null);

const handleRegister = async (formData) => {
  error.value = null;
  try {
    await api.registerUser(formData);
    router.push('/login');
  } catch (e) {
    console.error('Registration error:', e.response.data);
    error.value = Object.values(e.response.data).join(', ');
  }
};
</script>

<template>
  <div>
    <AuthForm formType="register" :submitForm="handleRegister" />
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
