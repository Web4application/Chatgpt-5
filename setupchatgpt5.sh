#!/bin/bash

# -----------------------------
# ChatGPT5 One-Command Setup
# -----------------------------

# 1. Check Python installation
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found! Please install Python 3.11+."
    exit 1
fi

# 2. Check Node.js installation
if ! command -v npm &>/dev/null; then
    echo "Node.js not found! Please install Node.js 18+."
    exit 1
fi

# 3. Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# 4. Install JS dependencies
if [ -f "package.json" ]; then
    echo "Installing JS dependencies..."
    npm install
fi

# 5. Create .env file if missing
if [ ! -f ".env" ]; then
    echo "Creating default .env file..."
    cat <<EOL > .env
GPT_API_KEY=your_api_key_here
BACKEND_PORT=5000
MEMORY_LIMIT=50
EOL
    echo ".env file created. Edit it with your GPT API key if needed."
fi

# 6. Start backend
echo "Starting ChatGPT5 backend..."
python3 ChatGPT5.py &
BACKEND_PID=$!

# 7. Wait for backend to initialize
sleep 5

# 8. Open web frontend if exists
if [ -f "ChatPage.js" ]; then
    echo "Opening web frontend in default browser..."
    # Simple HTML wrapper
    if [ ! -f "index.html" ]; then
        echo "<!DOCTYPE html>
<html>
<head>
    <title>ChatGPT5</title>
</head>
<body>
<script src='ChatPage.js'></script>
</body>
</html>" > index.html
    fi
    xdg-open index.html 2>/dev/null || open index.html
fi

echo "ChatGPT5 is running. Backend PID: $BACKEND_PID"
echo "Press Ctrl+C to stop."
wait $BACKEND_PID
