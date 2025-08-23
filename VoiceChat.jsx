import React, { useState, useEffect, useRef } from 'react';

const VoiceChat = ({ message }) => {
  const synth = window.speechSynthesis;
  const [speaking, setSpeaking] = useState(false);
  const utteranceRef = useRef(null);

  useEffect(() => {
    if (message && synth && !speaking) {
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.lang = 'en-US';
      utterance.pitch = 1;
      utterance.rate = 1;
      utterance.volume = 1;
      utterance.onstart = () => setSpeaking(true);
      utterance.onend = () => setSpeaking(false);
      synth.cancel(); // cancel any queued speech
      synth.speak(utterance);
      utteranceRef.current = utterance;
    }
  }, [message]);

  const stopSpeaking = () => {
    synth.cancel();
    setSpeaking(false);
  };

  return (
    <div>
      {speaking && <button onClick={stopSpeaking}>Stop Voice</button>}
    </div>
  );
};

export default VoiceChat;