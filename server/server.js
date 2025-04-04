const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
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
    
    // Call Python script to process message
    const pythonProcess = spawn('python', [
      path.join(__dirname, '../backend/process_message.py'),
      message
    ]);
    
    let responseData = '';
    
    pythonProcess.stdout.on('data', (data) => {
      responseData += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      const errorMessage = data.toString();
      console.error(`Python Error: ${errorMessage}`);
      
      // If we see an import error, provide more context
      if (errorMessage.includes('ModuleNotFoundError')) {
        console.log('Import error detected. Make sure all Python modules are correctly installed and paths are set properly.');
      }
    });
    
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python process exited with code ${code}`);
        return res.status(500).json({ 
          error: 'Error processing message',
          message: 'I encountered an error while processing your request. Please try again.'
        });
      }
      
      try {
        const parsedResponse = JSON.parse(responseData);
        
        // Check if the response contains an error
        if (parsedResponse.error) {
          console.error('Python error:', parsedResponse.error);
          if (parsedResponse.details) {
            console.error('Error details:', parsedResponse.details);
          }
          
          return res.status(500).json({ 
            error: parsedResponse.error,
            message: 'The AI assistant encountered a problem. Please try again later.'
          });
        }
        
        return res.json(parsedResponse);
      } catch (e) {
        console.error('Failed to parse JSON response:', e);
        console.error('Raw response:', responseData);
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

// Catch-all handler to serve React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/build/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 