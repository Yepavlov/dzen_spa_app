<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import api from '@/services/api.js';
import CommentForm from './CommentForm.vue';

const comments = ref([]);
const error = ref(null);
const replyToId = ref(null);
const expandedReplies = ref({});
const currentPage = ref(1);
const totalComments = ref(0);
const pageSize = 25;
const sortKey = ref('created_at');
const sortOrder = ref('desc');

const fetchComments = async () => {
  try {
    const params = {
      page: currentPage.value,
      ordering: `${sortOrder.value === 'desc' ? '-' : ''}${sortKey.value}`
    };
    const response = await api.getComments(params);
    comments.value = response.data.results;
    totalComments.value = response.data.count;
    error.value = null;
  } catch (e) {
    console.error('Error loading comments:', e);
    error.value = 'Unable to load comments.';
  }
};

let socket = null;

onMounted(() => {
  fetchComments();

  socket = new WebSocket('ws://localhost:8000/ws/comments/');

  socket.onopen = () => {
    console.log('WebSocket connection established.');
  };

  socket.onmessage = (event) => {
    console.log('WebSocket message received:', event.data);
    fetchComments();
  };

  socket.onclose = () => {
    console.log('WebSocket connection closed.');
  };

  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
});

onUnmounted(() => {
  if (socket) {
    socket.close();
  }
});


const totalPages = computed(() => Math.ceil(totalComments.value / pageSize));

const toggleReplyForm = (commentId) => {
  replyToId.value = replyToId.value === commentId ? null : commentId;
};

const toggleReplies = async (comment) => {
  const commentId = comment.id;

  if (comment.replies) {
    expandedReplies.value[commentId] = !expandedReplies.value[commentId];
    return;
  }

  try {
    const response = await api.getCommentDetails(commentId);
    const targetComment = comments.value.find(c => c.id === commentId);
    if (targetComment) {
      targetComment.replies = response.data.replies;
    }
    expandedReplies.value[commentId] = true;
  } catch (e) {
    console.error(`Unable to load replies for comment ${commentId}:`, e);
  }
};


const handleCommentPosted = () => {
  replyToId.value = null;
  fetchComments();
};

const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  fetchComments();
};

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'desc';
  }
  fetchComments();
};

defineExpose({ fetchComments });
</script>

<template>
  <div class="comments-container">
    <h1>Comments</h1>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="comments-table">
        <thead>
          <tr>
            <th @click="sortBy('author__username')">User Name ↕️</th>
            <th @click="sortBy('author__email')">E-mail ↕️</th>
            <th @click="sortBy('created_at')">Date ↕️</th>
            <th>Comment</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="comments.length === 0">
            <td colspan="4" style="text-align: center;">No comments yet.</td>
          </tr>
          <template v-for="comment in comments" :key="comment.id">
            <tr class="comment-row">
              <td>{{ comment.author_name }}</td>
              <td>{{ comment.author_email || 'hidden' }}</td>
              <td>{{ new Date(comment.created_at).toLocaleString() }}</td>
              <td>
                <p v-html="comment.text"></p>
                <button @click="toggleReplies(comment)" v-if="comment.replies_count > 0" class="toggle-replies-btn">
                  {{ expandedReplies[comment.id] ? 'Hide' : 'Show' }} Replies ({{ comment.replies_count }})
                </button>
                <button @click="toggleReplyForm(comment.id)" class="reply-btn">Reply</button>
              </td>
            </tr>
            <tr v-if="expandedReplies[comment.id] || replyToId === comment.id" class="replies-row">
              <td colspan="4">
                <div class="replies-container">
                    <div v-if="replyToId === comment.id" class="reply-form">
                        <CommentForm :parent-id="comment.id" @comment-posted="handleCommentPosted" />
                    </div>
                    <div v-if="expandedReplies[comment.id] && comment.replies">
                      <div v-for="reply in comment.replies" :key="reply.id" class="comment-item reply-item">
                        <div class="comment-header">
                          <strong>{{ reply.author_name }}</strong>
                          <span class="comment-date">{{ new Date(reply.created_at).toLocaleString() }}</span>
                        </div>
                        <p class="comment-text" v-html="reply.text"></p>
                      </div>
                    </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
      <div class="pagination">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">« Prev</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">Next »</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comments-container{max-width:800px;margin:2rem auto;padding:1rem;font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;color:#e0e0e0;background-color:#1a1a1a;border-radius:8px}.comments-table{width:100%;border-collapse:collapse;margin-top:1rem}.comments-table th,.comments-table td{border:1px solid #444;padding:.75rem;text-align:left;vertical-align:top}.comments-table th{cursor:pointer;background-color:#333}.comment-row:hover{background-color:#2a2a2a}.replies-row td{padding:0;border:none;border-left:1px solid #444;border-right:1px solid #444;border-bottom:1px solid #444}.replies-container{padding:1rem;background-color:#252525}.toggle-replies-btn{margin-right:10px;background-color:#444}.pagination{margin-top:1.5rem;display:flex;justify-content:center;align-items:center;gap:1rem}.pagination button{padding:.5rem 1rem;border:1px solid #555;background:#333;color:#fff;cursor:pointer}.pagination button:disabled{opacity:.5;cursor:not-allowed}.reply-btn{background:linear-gradient(135deg,#0066cc,#0052a3);border:none;color:#fff;padding:.5rem 1rem;cursor:pointer;border-radius:4px;margin-top:.5rem;font-size:.9em;transition:background .2s ease}.reply-btn:hover{background:linear-gradient(135deg,#0052a3,#004080)}
</style>
