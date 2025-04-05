# Healthcare Assistant Deployment Guide

This guide provides instructions for deploying the Healthcare Assistant application to a production server.

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Required Python packages (see requirements.txt)
- A web server (e.g., Nginx, Apache) for production deployments

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/EPICS-Repo.git
cd EPICS-Repo
```

### 2. Install Dependencies

```bash
# Install Node.js dependencies for the server
cd server
npm install --production

# Install Node.js dependencies for the frontend and build
cd ../frontend
npm install
npm run build

# Install Python dependencies
cd ..
pip install -r requirements.txt
```

### 3. Configure the Application

Create or edit the `.env` file in the root directory:

