import axios from 'axios';
import auth from '@/store/auth.js';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

apiClient.interceptors.response.use(response => response, error => {
    if (error.response && error.response.status === 401) {
        auth.logout();
    }
    return Promise.reject(error);
});


export default {
  getComments(params) {
    return apiClient.get('/api/comments/', { params });
  },
  registerUser(data) {
    return apiClient.post('/auth/users/', data);
  },
  loginUser(data) {
    return apiClient.post('/auth/jwt/create/', data);
  },
  getCaptcha() {
        return apiClient.get('/api/captcha/');
    },
  createComment(data) {
    return apiClient.post('/api/comments/', data);
  }
};
