import { B2BIdentityProvider } from '@stytch/react/b2b';

export const ConsentForm = () => {
  console.log('Rendering ConsentForm component');
  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="header-wrapper">
          <h1 className="page-heading">Welcome!</h1>
          <p className="page-subheading">
            Please provide your consent before using our Explain Like I'm Five LLM chatbot.
          </p>
        </div>
      </div>
      <B2BIdentityProvider />
    </div>
  );
};
