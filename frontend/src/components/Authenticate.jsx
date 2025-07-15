import { useStytchMemberSession } from '@stytch/react/b2b';
import { Navigate } from 'react-router-dom';
import { LogInOrSignUp } from './LogInOrSignUp';

export const Authenticate = () => {
  const { session } = useStytchMemberSession();

  if (session) {
    return <Navigate to={'/dashboard'} replace />;
  }

  return <LogInOrSignUp />;
};
