# Build script for Render deployment
#!/bin/bash

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies for frontend
echo "Installing Node.js dependencies..."
cd client
npm install
echo "Building frontend..."
npm run build
cd ..

echo "Build completed successfully!"
