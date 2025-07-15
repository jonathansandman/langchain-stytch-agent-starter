import { useStytchOrganization, useStytchMember } from '@stytch/react/b2b';
import { useStytchB2BClient } from '@stytch/react/b2b';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { consentUrl } from '../utils/stytchConfig';

export const ConsentRequiredRoutes = () => {
  const { organization } = useStytchOrganization();
  const { member } = useStytchMember();
  const stytch = useStytchB2BClient();
  const location = useLocation();

  const [consentGranted, setConsentGranted] = useState(null); // null = loading

  const isOnConsentPage = location.pathname.startsWith('/consent');

  useEffect(() => {
    const checkConsent = async () => {
      try {
        const tokens = stytch.session.getTokens();
        const sessionToken = tokens?.session_token;

        if (!organization || !member || !sessionToken) {
          console.log('⏳ Waiting for org, member, or token');
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
        console.log('✅ Connected apps:', hasConnectedApps);
        setConsentGranted(hasConnectedApps);
      } catch (error) {
        console.error('Error checking connected apps:', error);
        setConsentGranted(false); // Fail closed
      }
    };

    checkConsent();
  }, [organization, member, stytch.session]);

  if (consentGranted === null) {
    return null; // or a loading spinner
  }

  if (!consentGranted && !isOnConsentPage) {
    return <Navigate to={consentUrl} replace />;
  }

  return <Outlet />;
};
