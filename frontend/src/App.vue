<script setup>
import { RouterLink, RouterView } from 'vue-router';
import auth from '@/store/auth.js';

const handleLogout = () => {
  auth.logout();
};
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <template v-if="!auth.state.isAuthenticated">
          <RouterLink to="/login">Log in</RouterLink>
          <RouterLink to="/register">Sing up</RouterLink>
        </template>
        <template v-else>
          <a href="#" @click.prevent="handleLogout">Log out</a>
        </template>
      </nav>
    </div>
  </header>
  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}
nav {
  width: 100%;
  font-size: 1rem;
  text-align: center;
  margin-top: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ccc;
}
nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}
nav a:first-of-type {
  border: 0;
}
</style>
