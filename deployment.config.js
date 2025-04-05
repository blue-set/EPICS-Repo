/**
 * Deployment configuration for the Healthcare Assistant
 * Update these settings according to your production environment
 */
module.exports = {
  // Server configuration
  server: {
    // The port for the server to listen on
    port: process.env.PORT || 5000,
    
    // Public URL of your deployed application (no trailing slash)
    // Example: 'https://healthcare-assistant.example.com'
    publicUrl: process.env.PUBLIC_URL || '',
    
    // Whether to enable detailed debugging logs
    debug: process.env.DEBUG === 'true' || false,
    
    // Allowed origins for CORS
    // Add your production domain(s) here
    allowedOrigins: [
      'http://localhost:3000',
      'http://localhost:5000',
      'http://127.0.0.1:3000',
      'http://127.0.0.1:5000',
      // Add your production domain here. For example:
      // 'https://healthcare-assistant.example.com',
      // For development with ngrok or similar:
      // 'https://*.ngrok.io',
      // Add your EC2 public IP address with port
      'http://13.57.201.14:5000',
      'http://13.57.201.14:3000'
    ]
  },
  
  // Python configuration
  python: {
    // Path to Python executable (if not in PATH)
    pythonPath: process.env.PYTHON_PATH || 'python',
    
    // Whether to log Python errors to the console
    logErrors: true,
    
    // Path to the backend script
    backendScript: '../backend/process_message.py',
  },
  
  // Timeouts
  timeouts: {
    // Maximum time to wait for a response from the Python backend (in milliseconds)
    pythonResponse: 30000,
  }
};
