import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
});

// Automatically attach the VIP badge
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// THE DEAD MAN'S SWITCH
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If the bouncer rejects the VIP badge (401), force logout
    if (error.response && error.response.status === 401) {
      console.log("VIP badge expired or invalid. Forcing logout.");
      localStorage.removeItem('token');
      localStorage.removeItem('disclaimer_accepted');
      // Force a hard refresh to clear broken state
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

export default api;