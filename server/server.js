const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config();

// Import deployment configuration
const config = require('../deployment.config');

// Make sure allowedOrigins includes your EC2 IP address
if (!config.server || !config.server.allowedOrigins) {
  config.server = config.server || {};
  config.server.allowedOrigins = config.server.allowedOrigins || [];
}

if (!config.server.allowedOrigins.includes('http://13.57.201.14:5000')) {
  config.server.allowedOrigins.push('http://13.57.201.14:5000');
  config.server.allowedOrigins.push('http://13.57.201.14:3000');
}

const app = express();
const PORT = config.server.port;

// Simple CORS configuration that allows all origins
app.use(cors());

// Comment out the original CORS configuration
/*
app.use(cors({
  origin: function(origin, callback) {
    if (!origin || config.server.allowedOrigins.includes(origin) || config.server.allowedOrigins.includes('*')) {
      callback(null, true);
    } else {
      console.log('CORS blocked for origin:', origin);
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
*/

app.use(bodyParser.json());

// Serve static files from React build
app.use(express.static(path.join(__dirname, '../frontend/build')));

// API Routes
app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }
    
    // Call Python script to process message using config
    const pythonProcess = spawn(config.python.pythonPath, [
      path.join(__dirname, config.python.backendScript),
      message
    ]);
    
    let responseData = '';
    let errorData = '';
    
    pythonProcess.stdout.on('data', (data) => {
      responseData += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      const errorMessage = data.toString();
      errorData += errorMessage;
      
      if (config.python.logErrors) {
        console.error(`Python Error: ${errorMessage}`);
      }
      
      // If we see an import error, provide more context
      if (errorMessage.includes('ModuleNotFoundError')) {
        console.log('Import error detected. Make sure all Python modules are correctly installed and paths are set properly.');
      }
    });
    
    // Set a timeout for the Python process
    const timeout = setTimeout(() => {
      pythonProcess.kill();
      res.status(504).json({ 
        error: 'Processing timeout',
        message: 'The request took too long to process. Please try again with a shorter message.'
      });
    }, config.timeouts.pythonResponse);
    
    pythonProcess.on('close', (code) => {
      clearTimeout(timeout); // Clear the timeout
      
      if (res.headersSent) {
        return; // Response already sent (e.g., by timeout)
      }
      
      if (code !== 0) {
        console.error(`Python process exited with code ${code}`);
        return res.status(500).json({ 
          error: 'Error processing message',
          message: 'I encountered an error while processing your request. Please try again.',
          details: errorData
        });
      }
      
      try {
        const parsedResponse = JSON.parse(responseData);
        
        // Check if the response contains an error
        if (parsedResponse.error) {
          if (config.server.debug) {
            console.error('Python error:', parsedResponse.error);
            if (parsedResponse.details) {
              console.error('Error details:', parsedResponse.details);
            }
          }
          
          return res.status(500).json({ 
            error: parsedResponse.error,
            message: 'The AI assistant encountered a problem. Please try again later.'
          });
        }
        
        return res.json(parsedResponse);
      } catch (e) {
        console.error('Failed to parse JSON response:', e);
        if (config.server.debug) {
          console.error('Raw response:', responseData);
        }
        return res.json({ message: responseData.trim() });
      }
    });
  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({ 
      error: 'Server error',
      message: 'Sorry, I encountered a server error. Please try again later.'
    });
  }
});

app.post('/api/clear-chat', (req, res) => {
  // This endpoint can be extended to clear any backend chat state if needed
  res.json({ success: true, message: 'Chat cleared successfully' });
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok',
    timestamp: new Date().toISOString(),
    serverInfo: {
      nodeVersion: process.version,
      platform: process.platform,
      memory: process.memoryUsage(),
    }
  });
});

// Environment info endpoint (disable in production)
if (process.env.NODE_ENV !== 'production') {
  app.get('/api/debug-info', (req, res) => {
    res.json({
      environment: process.env.NODE_ENV || 'development',
      serverTime: new Date().toISOString(),
      config: {
        port: PORT,
        pythonPath: config.python.pythonPath,
        allowedOrigins: config.server.allowedOrigins,
      }
    });
  });
}

// Catch-all handler to serve React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/build/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});