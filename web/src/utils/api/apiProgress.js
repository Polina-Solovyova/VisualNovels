import axios from 'axios';

// URL для запросов
const API_URL = 'http://localhost:8000/api/progress/';

// Сохранение прогресса пользователя
export const saveProgress = async (progressData) => {
    try {
        const response = await axios.post(API_URL, progressData);
        return response.data;
    } catch (error) {
        throw error;
    }
};
