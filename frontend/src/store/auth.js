import { reactive, readonly } from 'vue';
import { useRouter } from 'vue-router';

const state = reactive({
  isAuthenticated: !!localStorage.getItem('authToken'),
  user: null //
});

const actions = {
  login(token) {
    localStorage.setItem('authToken', token);
    state.isAuthenticated = true;
  },
  logout() {
    localStorage.removeItem('authToken');
    state.isAuthenticated = false;
    state.user = null;
    window.location.href = '/login';
  }
};

export default {
  state: readonly(state),
  ...actions
};
