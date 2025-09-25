%pip install --upgrade "openai>=1.88" "openai-agents>=0.0.19"
pip install -r requirements.txt

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install torch transformers fastapi uvicorn
pip install torch --index-url https://download.pytorch.org/whl/cu118
npm install
npm start
