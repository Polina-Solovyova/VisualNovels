import axios from 'axios';
import Cookies from 'universal-cookie';

const cookies = new Cookies();
const API_URL = 'http://localhost:8000/api/';

const axiosInstance = axios.create({
    baseURL: API_URL,
    timeout: 1000,
});

axiosInstance.interceptors.request.use(config => {
    const token = cookies.get('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

export const getNovels = async () => {
    const token = cookies.get('access_token');

    if (!token) {
        throw new Error('No access token found');
    }

    console.log('Access Token:', token);

    const response = await axios.get(API_URL, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    return response.data;
};


export const getNovelDetails = async (novelId) => {
    try {
        const response = await axiosInstance.get(`${API_URL}/api/${novelId}/`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// Получение списка эпизодов
export const getEpisodeList = async (novelId) => {
    try {
        const response = await axiosInstance.get(`${API_URL}/api/novel/${novelId}/episodes/`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// Получение конкретного эпизода
export const getEpisode = async (novelId, episodeId) => {
    try {
        const response = await axiosInstance.get(`${API_URL}/novel/${novelId}/episode/${episodeId}/`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

// Получение текущего диалога
export const getCurrentDialogue = async (novelId) => {
    try {
        const response = await axiosInstance.get(`/novel/${novelId}/current-dialogue/`);
        return response.data; // Ожидаем корректные данные
    } catch (error) {
        console.error('Error fetching current dialogue:', error);
        throw error;
    }
};

// Обновление прогресса для получения следующего диалога
export const updateProgress = async (novelId) => {
    try {
        const response = await axiosInstance.post(`/novel/${novelId}/update-progress/`, { save_progress: true });
        return response.data;
    } catch (error) {
        console.error('Error updating progress:', error);
        throw error;
    }
};

