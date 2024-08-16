import axios from 'axios';

const API_URL = 'http://localhost:8000/api/progress/';

export const saveProgress = async (progressData) => {
    try {
        const response = await axios.post(API_URL, progressData);
        return response.data;
    } catch (error) {
        throw error;
    }
};
