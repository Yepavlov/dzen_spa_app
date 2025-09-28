<template>
  <div v-if="comment">
    <h1>Comment by {{ comment.author_name }}</h1>
    <p v-html="comment.text"></p>
    <hr>
    <h3>Replies:</h3>
    <div v-if="comment.replies && comment.replies.length > 0">
      <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
        <strong>{{ reply.author_name }}</strong>:
        <p v-html="reply.text"></p>
      </div>
    </div>
    <p v-else>No replies yet.</p>
  </div>
  <div v-else-if="error">
    <p>{{ error }}</p>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api.js';

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  }
});

const comment = ref(null);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await api.getCommentDetails(props.id);
    comment.value = response.data;
  } catch (e) {
    console.error('Failed to load comment details:', e);
    error.value = 'Failed to load comment details.';
  }
});
</script>

<style scoped>
.reply-item {
  border-left: 2px solid #ccc;
  padding-left: 15px;
  margin-left: 10px;
  margin-bottom: 10px;
}
</style>
