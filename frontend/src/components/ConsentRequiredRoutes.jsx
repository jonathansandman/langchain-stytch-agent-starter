import { useStytchOrganization, useStytchMember, useStytchMemberSession } from '@stytch/react/b2b';
import { useStytchB2BClient } from '@stytch/react/b2b';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { consentUrl } from '../utils/stytchConfig';

export const ConsentRequiredRoutes = () => {
  const { organization } = useStytchOrganization();
  const { member } = useStytchMember();
  const { session } = useStytchMemberSession();
  const stytch = useStytchB2BClient();
  const location = useLocation();
  const [consentGranted, setConsentGranted] = useState(null); // null = loading
  const isOnConsentPage = location.pathname.startsWith('/consent');

  const role = session?.roles.includes('stytch_admin') ? 'admin' : 'member';
  const isAuthorizedToViewRecentTopics = stytch.rbac.isAuthorizedSync('explain.topic', 'read');

  if (role !== 'admin' && isAuthorizedToViewRecentTopics) {
    return <Outlet />;
  }

  useEffect(() => {
    const checkConsent = async () => {
      try {
        const tokens = stytch.session.getTokens();
        const sessionToken = tokens?.session_token;

        if (!organization || !member || !sessionToken) {
          return;
        }

        const response = await stytch.self.getConnectedApps(
          {
            organization_id: organization.organization_id,
            member_id: member.member_id,
          },
          {
            authorization: { session_token: sessionToken },
          }
        );

        const hasConnectedApps = response.connected_apps?.length > 0;
        setConsentGranted(hasConnectedApps);
      } catch (error) {
        setConsentGranted(false);
      }
    };

    checkConsent();
  }, [organization, member, stytch.session]);

  if (consentGranted === null) {
    return null;
  }

  if (!consentGranted && !isOnConsentPage) {
    return <Navigate to={consentUrl} replace />;
  }

  return <Outlet />;
};
