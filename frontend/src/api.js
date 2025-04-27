// frontend/src/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await axios.post(`${API_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading document:', error);
    throw error;
  }
};

export const sendMessage = async (message) => {
  try {
    const response = await axios.post(`${API_URL}/chat`, { message });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export const deleteAllDocuments = async () => {
  try {
    const response = await axios.delete(`${API_URL}/delete`);
    return response.data;
  } catch (error) {
    console.error('Error deleting documents:', error);
    throw error;
  }
};


export const getDocuments = async () => {
  const response = await fetch('http://localhost:8000/documents');
  if (!response.ok) {
    throw new Error('Failed to fetch documents');
  }
  return response.json();
};