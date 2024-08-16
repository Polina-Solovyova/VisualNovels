import axios from 'axios';
import Cookies from 'universal-cookie';

const cookies = new Cookies();
const API_URL = 'http://localhost:8000/api/';

// Создаем экземпляр axios
const axiosInstance = axios.create({
    baseURL: API_URL,
    timeout: 1000,
});

// Добавляем интерцептор для установки заголовка Authorization
axiosInstance.interceptors.request.use(
    config => {
        const token = cookies.get('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Получение списка новелл
export const getNovels = async () => {
    try {
        const response = await axiosInstance.get('/');
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 401) {
            // Неавторизованный запрос, возможно токен истек или отсутствует
            console.error('Authorization error: ', error);
            // Выполните действия по очистке токена и/или перенаправлению
            cookies.remove('access_token');
            cookies.remove('refresh_token');
            // Например, перенаправление на страницу входа
            window.location.href = '/login';
        } else {
            console.error('Error fetching novels:', error);
        }
        throw error;
    }
};

export default axiosInstance;
