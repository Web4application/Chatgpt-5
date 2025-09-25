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

curl -X 'POST' \
'http://0.0.0.0:8000/v1/chat/completions' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
    "model": "meta/llama-3.1-70b-instruct",
    "messages": [{"role":"user", "content":"Write a limerick about the wonders of GPU computing."}],
    "max_tokens": 64
}'

export NGC_API_KEY=<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>
export LOCAL_NIM_CACHE=~/.cache/nim
mkdir -p "$LOCAL_NIM_CACHE"
docker run -it --rm \
    --gpus all \
    --shm-size=16GB \
    -e NGC_API_KEY \
    -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
    -u $(id -u) \
    -p 8000:8000 \
    nvcr.io/nim/meta/llama-3.1-70b-instruct:latest
