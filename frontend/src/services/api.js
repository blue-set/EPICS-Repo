const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const fetchBotResponse = async (message) => {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};

export const clearChat = async () => {
  try {
    const response = await fetch(`${API_URL}/clear-chat`, {
      method: 'POST',
    });
    
    if (!response.ok) {
      throw new Error('Failed to clear chat');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Clear chat error:', error);
    throw error;
  }
}; 