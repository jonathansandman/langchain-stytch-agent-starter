import { useState } from 'react';
import './form.css';

const ExplainForm = () => {
  const [topic, setTopic] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const baseUrl = import.meta.env.VITE_SERVER_BASE_URL || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/explain`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ', // We'll add our token here!
        },
        body: JSON.stringify({ topic }),
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (err) {
      console.error(err);
      setResponse('Error: Could not fetch explanation.');
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <label htmlFor="topic">Topic:</label>
        <input
          type="text"
          placeholder="Enter a topic..."
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <button type="submit">Explain it to me like I’m 5</button>
      </form>
      {response && <div className="response-box">{response}</div>}
    </div>
  );
};

export default ExplainForm;
