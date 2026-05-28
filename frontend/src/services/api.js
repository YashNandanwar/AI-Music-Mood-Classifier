import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

export const predictMood = async (data) => {
    try {
        const response = await axios.post(`${API_URL}/predict`, data);
        return response.data;
    } catch (error) {
        console.error('Error predicting mood:', error);
        throw error;
    }
};

export const predictMoodByName = async (songName) => {
    try {
        const response = await axios.post(`${API_URL}/predict-by-name`, { song_name: songName });
        return response.data;
    } catch (error) {
        console.error('Error predicting mood by name:', error);
        throw error;
    }
};

export const getHistory = async () => {
    try {
        const response = await axios.get(`${API_URL}/history`);
        return response.data;
    } catch (error) {
        console.error('Error fetching history:', error);
        throw error;
    }
};

export const clearHistory = async () => {
    try {
        const response = await axios.delete(`${API_URL}/history`);
        return response.data;
    } catch (error) {
        console.error('Error clearing history:', error);
        throw error;
    }
};
