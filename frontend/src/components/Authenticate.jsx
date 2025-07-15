import { useStytchMemberSession } from '@stytch/react/b2b';
import { Navigate } from 'react-router-dom';
import { LogInOrSignUp } from './LogInOrSignUp';
import { dashboardConsentUrl } from '../utils/stytchConfig';

export const Authenticate = () => {
  const { session } = useStytchMemberSession();

  if (session) {
    return <Navigate to={dashboardConsentUrl} replace />;
  }

  return <LogInOrSignUp />;
};
