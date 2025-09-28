<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api.js';

const text = ref('');
const captchaKey = ref('');
const captchaValue = ref('');
const captchaImage = ref('');
const error = ref(null);
const imageFile = ref(null);
const textFile = ref(null);

const emit = defineEmits(['comment-posted']);

const props = defineProps({
  parentId: {
    type: Number,
    default: null
  }
});


const fetchCaptcha = async () => {
  try {
    const response = await api.getCaptcha();
    captchaKey.value = response.data.key;
    captchaImage.value = response.data.image_url;
  } catch (e) {
    console.error("Unable to load CAPTCHA", e);
  }
};

const handleImageChange = (e) => {
  imageFile.value = e.target.files[0];
};

const handleTextFileChange = (e) => {
  textFile.value = e.target.files[0];
};


const handleSubmit = async () => {
  error.value = null;

  const formData = new FormData();
  formData.append('text', text.value);
  formData.append('captcha_key', captchaKey.value);
  formData.append('captcha_value', captchaValue.value);


  if (props.parentId) {
    formData.append('parent', props.parentId);
  }

  if (imageFile.value) {
    formData.append('image', imageFile.value);
  }
  if (textFile.value) {
    formData.append('text_file', textFile.value);
  }

  try {
    await api.createComment(formData);
    text.value = '';
    captchaValue.value = '';
    imageFile.value = null;
    textFile.value = null;

    const imageInput = document.getElementById('image-upload');
    if (imageInput) imageInput.value = '';
    const textFileInput = document.getElementById('text-file-upload');
    if (textFileInput) textFileInput.value = '';

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

      <div class="file-inputs">
        <div>
          <label for="image-upload">Add an image:</label>
          <input id="image-upload" type="file" @change="handleImageChange" accept="image/png, image/jpeg, image/gif">
        </div>
        <div>
          <label for="text-file-upload">Add a text file:</label>
          <input id="text-file-upload" type="file" @change="handleTextFileChange" accept=".txt">
        </div>
      </div>

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
.file-inputs {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}
</style>
