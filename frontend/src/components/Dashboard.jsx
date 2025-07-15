import { useStytchMemberSession, useStytchOrganization, useStytchMember } from '@stytch/react/b2b';
import { useStytchB2BClient, B2BIdentityProvider } from '@stytch/react/b2b';

import { useEffect, useState } from 'react';
import ExplainForm from './ExplainForm';
import { useRecentTopics } from '../utils/useRecentTopics';

export const Dashboard = () => {
  const { session } = useStytchMemberSession();
  const { organization } = useStytchOrganization();
  const { member } = useStytchMember();
  const stytch = useStytchB2BClient();

  const [sessionTokens, setSessionTokens] = useState({});
  const [consentGrantedToChatbot, setConsentGrantedToChatbot] = useState(false);

  const { recentTopics, setRecentTopics, addTopic } = useRecentTopics([]);
  const isAuthorizedToViewRecentTopics = stytch.rbac.isAuthorizedSync('explain.topic', 'read');

  const handleGetTokens = () => {
    const tokens = stytch.session.getTokens();
    setSessionTokens(tokens);
  };

  const role = session?.roles.includes('stytch_admin') ? 'admin' : 'member';

  useEffect(() => {
    if (stytch?.session) {
      handleGetTokens();
    }
  }, []);

  // See if user has connected apps
  useEffect(() => {
    const params = {
      organization_id: organization?.organization_id,
      member_id: member?.member_id,
    };

    const options = {
      authorization: {
        session_token: sessionTokens?.session_token,
      },
    };

    stytch.self
      .getConnectedApps(params, options)
      .then((response) => {
        if (response.connected_apps.length > 0) {
          setConsentGrantedToChatbot(true);
        } else {
          console.log('No connected apps found for this user.');
          setConsentGrantedToChatbot(false);
        }
      })
      .catch((error) => {
        console.error('Error fetching connected apps:', error);
      });
  }, [sessionTokens, organization, member]);

  useEffect(() => {
    if (!sessionTokens?.session_token) {
      console.warn('Session token not ready, skipping fetch');
      return;
    }

    const baseUrl = import.meta.env.VITE_SERVER_BASE_URL || 'http://localhost:8000';
    fetch(`${baseUrl}/topics-and-explanations`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${sessionTokens.session_token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // set recent topics to the most recent 5 topics from data response
        setRecentTopics(recentTopics.length > 0 ? recentTopics : data?.slice(-5));
      })
      .catch((error) => {
        console.error('Error fetching topics:', error);
      });
  }, [sessionTokens]);

  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="header-wrapper">
          <h1 className="page-heading">Welcome, {organization?.organization_name}!</h1>
          <p className="page-subheading">
            You’re logged in as an <strong>{role}</strong>. This space is private to your
            organization’s members.
          </p>
        </div>
      </div>
      {consentGrantedToChatbot ? (
        <ExplainForm sessionToken={sessionTokens?.session_token} addTopic={addTopic} />
      ) : (
        <B2BIdentityProvider />
      )}
      {isAuthorizedToViewRecentTopics && (
        <div className="topics-list">
          <h2>Organization members' last 5 topics</h2>
          {recentTopics?.length > 0 ? (
            <ul>
              {recentTopics.map((topic, index) => (
                <li key={index}>
                  <strong>{topic.topic}</strong>: {topic.explanation}
                </li>
              ))}
            </ul>
          ) : (
            <p>No recent topics searched</p>
          )}
        </div>
      )}
    </div>
  );
};
