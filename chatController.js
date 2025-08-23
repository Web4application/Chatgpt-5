// Placeholder controller for chat-related logic
const sendMessage = (req, res) => {
  const { username, text } = req.body;
  // Handle sending messages, maybe store in the database
  res.status(200).send({ username, text });
};

module.exports = { sendMessage };
