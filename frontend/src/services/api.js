import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('uab_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = (email, password) => {
  const data = new URLSearchParams();
  data.append('username', email);
  data.append('password', password);
  return api.post('/auth/login', data);
};

export const register = (payload) => api.post('/auth/register', payload);

export const sendChat = (message) => api.post('/chat', { message });

export const uploadPdf = (file) => {
  const data = new FormData();
  data.append('file', file);
  return api.post('/upload-pdf', data);
};

export const getAnalytics = async () => {
  const [cgpa, pass, risk, dist] = await Promise.all([
    api.get('/analytics/department-cgpa'),
    api.get('/analytics/pass-rate'),
    api.get('/analytics/at-risk'),
    api.get('/analytics/cgpa-distribution'),
  ]);

  return {
    cgpa: cgpa.data,
    pass: pass.data,
    risk: risk.data,
    dist: dist.data,
  };
};

export default api;
