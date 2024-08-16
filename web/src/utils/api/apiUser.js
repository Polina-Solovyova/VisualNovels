import axios from 'axios';
import Cookies from 'universal-cookie';

const cookies = new Cookies();
const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const API_USER = {
  uploadAvatar: async (formData) => {
    const token = cookies.get('access_token');
    try {
      const response = await api.post('/api/upload-avatar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error('API uploadAvatar error:', error);
      throw error;
    }
  },

  getUserProfile: async () => {
    const token = cookies.get('access_token');
    try {
      const response = await api.get('/api/profile/', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error('API getUserProfile error:', error);
      throw error;
    }
  },

  getNovelsByIds: async (ids) => {
    const token = cookies.get('access_token');
    try {
      const response = await api.post('/api/novels/', { ids }, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching novels by IDs:', error);
      throw error;
    }
  },
};
