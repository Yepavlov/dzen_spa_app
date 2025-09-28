<script setup>
import { ref } from 'vue';
import CommentList from '@/components/CommentList.vue';
import CommentForm from '@/components/CommentForm.vue';
import auth from '@/store/auth.js';

const commentListRef = ref(null);

const handleCommentPosted = () => {
  if (commentListRef.value) {
    commentListRef.value.fetchComments();
  }
};
</script>

<template>
  <main>
    <CommentForm v-if="auth.state.isAuthenticated" @comment-posted="handleCommentPosted" />
    <CommentList ref="commentListRef" />
  </main>
</template>
