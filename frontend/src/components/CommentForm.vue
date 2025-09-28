<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api.js';

const text = ref('');
const captchaKey = ref('');
const captchaValue = ref('');
const captchaImage = ref('');
const error = ref(null);

const emit = defineEmits(['comment-posted']);

const fetchCaptcha = async () => {
  try {
    const response = await api.getCaptcha();
    captchaKey.value = response.data.key;
    captchaImage.value = response.data.image_url;
  } catch (e) {
    console.error("Unable to load CAPTCHA", e);
  }
};

const handleSubmit = async () => {
  error.value = null;
  try {
    await api.createComment({
      text: text.value,
      captcha_key: captchaKey.value,
      captcha_value: captchaValue.value,
    });
    text.value = '';
    captchaValue.value = '';
    emit('comment-posted');
    fetchCaptcha();
  } catch (e) {
    console.error('Error sending comment:', e.response.data);
    error.value = Object.values(e.response.data).join(' ');
    fetchCaptcha();
  }
};

onMounted(fetchCaptcha);
</script>

<template>
  <div class="form-container">
    <h3>Leave a comment</h3>
    <form @submit.prevent="handleSubmit">
      <textarea v-model="text" placeholder="Your comment..." required></textarea>
      <div class="captcha-container" v-if="captchaImage">
        <img :src="`http://localhost:8000${captchaImage}`" alt="CAPTCHA">
        <input type="text" v-model="captchaValue" placeholder="Enter the text from the image" required>
        <button type="button" @click="fetchCaptcha">Refresh</button>
      </div>
      <button type="submit">Send</button>
    </form>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<style scoped>
.form-container {
  margin-top: 2rem;
  padding: 1rem;
  border-top: 1px solid #ccc;
}
textarea {
  width: 100%;
  min-height: 100px;
  padding: 0.5rem;
  margin-bottom: 1rem;
}
.captcha-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.error-message {
  color: red;
}
</style>
