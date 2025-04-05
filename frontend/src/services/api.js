const API_URL = '/api';  // Use relative path instead of absolute URL with hostname

// Add a helper function to check server connectivity
export const checkServerHealth = async () => {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) {
      throw new Error(`Server health check failed: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Server health check failed:', error);
    throw error;
  }
};

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
      // Try to get error details from the response
      try {
        const errorData = await response.json();
        throw new Error(errorData.error || errorData.message || 'Network response was not ok');
      } catch (jsonError) {
        // If we can't parse the JSON, throw a generic error with the status
        throw new Error(`Server error: ${response.status}`);
      }
    }
    
    return await response.json();
  } catch (error) {
    console.error('API error:', error);
    // Check if it's a network error (likely server connection issue)
    if (error.message === 'Failed to fetch') {
      throw new Error('Server connection failed. Please check if the server is running and accessible.');
    }
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