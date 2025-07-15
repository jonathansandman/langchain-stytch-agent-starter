import { AdminPortalB2BProducts } from '@stytch/react/b2b/adminPortal';
import { AuthFlowType, B2BProducts, B2BOAuthProviders } from '@stytch/vanilla-js';

export const adminPortalConfig = {
  allowedAuthMethods: [
    AdminPortalB2BProducts.emailMagicLinks,
    AdminPortalB2BProducts.sso,
    AdminPortalB2BProducts.oauthGoogle,
  ],
  getRoleDescription: (role) => {
    if (role.role_id == 'stytch_admin') {
      return 'Able to manage settings, members, and search topics';
    } else if (role.role_id == 'stytch_member') {
      return 'Able to view settings, members, and recent search topics, but cannot search topics of their own or add new members';
    } else {
      return role.description;
    }
  },
  getRoleDisplayName: (role) => {
    if (role.role_id == 'stytch_admin') {
      return 'Admin';
    } else if (role.role_id == 'stytch_member') {
      return 'Member';
    } else {
      return role.role_id;
    }
  },
};

export const discoveryConfig = {
  products: [B2BProducts.sso, B2BProducts.oauth, B2BProducts.emailMagicLinks],
  sessionOptions: { sessionDurationMinutes: 60 },
  oauthOptions: {
    providers: [{ type: B2BOAuthProviders.Google }],
  },
  authFlowType: AuthFlowType.Discovery,
};

export const adminPortalStyles = {
  fontFamily: 'IBM Plex Sans',
};

export const discoveryStyles = {
  fontFamily: 'IBM Plex Sans',
  container: {
    width: '500px',
  },
};

const CONNECTED_APP_CLIENT_ID = import.meta.env.VITE_CONNECTED_APP_CLIENT_ID;
const CONNECTED_APP_REDIRECT_URI = import.meta.env.VITE_CONNECTED_APP_REDIRECT_URI;

export const dashboardConsentUrl = `/dashboard?client_id=${CONNECTED_APP_CLIENT_ID}&redirect_uri=${encodeURIComponent(CONNECTED_APP_REDIRECT_URI)}`;
