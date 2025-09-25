import express from 'express';
import fetch from 'node-fetch';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

// GPT-5 Mini chat endpoint
app.post('/api/chat', async (req, res) => {
  const { message } = req.body;
  try {
    const response = await fetch('https://api.mini-gpt5.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer YOUR_GPT5_MINI_KEY', // <-- Replace with your key
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'gpt-5mini',
        messages: [{ role: 'user', content: message }]
      })
    });

    const data = await response.json();
    const reply = data.choices[0].message.content;
    res.json({ reply });

  } catch (err) {
    console.error(err);
    res.status(500).json({ reply: 'Error connecting to GPT-5 Mini API' });
  }
});

// Ethereum info endpoint
app.get('/api/eth/:address', async (req, res) => {
  const address = req.params.address;
  const ETHERSCAN_KEY = 'YOUR_ETHERSCAN_API_KEY'; // <-- Replace with your key

  try {
    // Fetch balance
    const balRes = await fetch(`https://api.etherscan.io/api?module=account&action=balance&address=${address}&tag=latest&apikey=${ETHERSCAN_KEY}`);
    const balData = await balRes.json();
    const balance = Number(balData.result)/1e18;

    // Fetch latest 5 transactions
    const txRes = await fetch(`https://api.etherscan.io/api?module=account&action=txlist&address=${address}&startblock=0&endblock=99999999&page=1&offset=5&sort=desc&apikey=${ETHERSCAN_KEY}`);
    const txData = await txRes.json();

    res.json({ balance, transactions: txData.result });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Error fetching Ethereum info' });
  }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`MotokoPilot backend running on port ${PORT}`));
