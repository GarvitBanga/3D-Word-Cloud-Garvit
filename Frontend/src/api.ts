import axios from 'axios';
const API_URL = 'http://localhost:8000';
export interface Topic {
    word: string;
    weight: number;
}
export interface AnalyzeResponse {
    topics: Topic[];
}
export const analyzeUrl = async (url: string): Promise<Topic[]> => {
    try {
        const response = await axios.post<AnalyzeResponse>(`${API_URL}/analyze`, { url });
        return response.data.topics;
    } catch (error) {
        console.error('Error analyzing URL:', error);
        throw error;
    }
};
