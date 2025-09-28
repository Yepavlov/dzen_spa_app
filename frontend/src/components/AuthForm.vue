<script setup>
import { ref } from 'vue';

const props = defineProps({
  formType: {
    type: String,
    required: true // 'login' or 'register'
  },
  submitForm: {
    type: Function,
    required: true
  }
});

const username = ref('');
const password = ref('');
const email = ref('');

const handleSubmit = () => {
  const formData = {
    username: username.value,
    password: password.value
  };
  if (props.formType === 'register') {
    formData.email = email.value;
  }
  props.submitForm(formData);
};
</script>

<template>
  <div class="auth-container">
    <h1>{{ formType === 'login' ? 'Login' : 'Registration' }}</h1>
    <form @submit.prevent="handleSubmit" class="auth-form">
      <div class="form-group">
        <label for="username">User name</label>
        <input id="username" v-model="username" type="text" required>
      </div>
      <div v-if="formType === 'register'" class="form-group">
        <label for="email">Email</label>
        <input id="email" v-model="email" type="email" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input id="password" v-model="password" type="password" required>
      </div>
      <button type="submit">{{ formType === 'login' ? 'Log in' : 'Sign up' }}</button>
    </form>
  </div>
</template>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.form-group {
  display: flex;
  flex-direction: column;
}
input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 0.75rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #2980b9;
}
</style>
