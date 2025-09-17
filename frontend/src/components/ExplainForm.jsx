import { useState } from 'react';
import './form.css';
import { useStytchIsAuthorized } from '@stytch/react/b2b';

const ExplainForm = (props) => {
  const { sessionToken, addTopic } = props;
  const [topic, setTopic] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const canSubmitTopic = useStytchIsAuthorized('explain.topic', 'create');

  // Show loading state while permissions are being checked
  if (canSubmitTopic === null) {
    return <div>Loading permissions...</div>;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const baseUrl = import.meta.env.VITE_SERVER_BASE_URL || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/explain`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${sessionToken}`,
        },
        body: JSON.stringify({ topic }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Failed to fetch explanation');
      }

      addTopic(topic, data.response);
      setResponse(data.response);
    } catch (err) {
      console.error(err);
      setResponse('Could not fetch explanation. Try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        {!canSubmitTopic && (
          <div className="error-message">
            You do not have permission to submit topics. Please contact your administrator.
          </div>
        )}
        <label htmlFor="topic">Topic:</label>
        <input
          disabled={!canSubmitTopic}
          type="text"
          placeholder="Enter a topic..."
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <button disabled={!canSubmitTopic || isLoading} type="submit">
          {isLoading ? (
            <>
              <span className="spinner"></span>
              Thinking...
            </>
          ) : (
            "Explain it to me like I'm 5"
          )}
        </button>
      </form>
      {response && <div className="response-box">{response}</div>}
    </div>
  );
};

export default ExplainForm;
