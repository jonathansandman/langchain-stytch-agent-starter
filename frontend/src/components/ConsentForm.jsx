import { B2BIdentityProvider } from '@stytch/react/b2b';

export const ConsentForm = () => {
  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="header-wrapper">
          <h1 className="page-heading">CLI Access Request</h1>
          <p className="page-subheading">
            The <strong>Eli5 History CLI</strong> tool is requesting permission to access your explanation history.
          </p>
          <p className="page-subheading">
            This will allow you to view your explanations from the command line.
          </p>
        </div>
      </div>
      <B2BIdentityProvider />
    </div>
  );
};
