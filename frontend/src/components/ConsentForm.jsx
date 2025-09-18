import { B2BIdentityProvider } from '@stytch/react/b2b';

export const ConsentForm = () => {
  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="header-wrapper">
          <h1 className="page-heading">Application Access Request</h1>
          <p className="page-subheading">
            An external application is requesting permission to access your data. Please review and choose whether to grant access.
          </p>
        </div>
      </div>
      <B2BIdentityProvider />
    </div>
  );
};
