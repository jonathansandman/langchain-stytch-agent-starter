// REPLACE entire file with simple session check
import { useStytchMemberSession } from '@stytch/react/b2b';
import { Navigate, Outlet } from 'react-router-dom';

export const ConsentRequiredRoutes = () => {
  const { session } = useStytchMemberSession();

  if (!session) {
    return <Navigate to="/authenticate" replace />;
  }

  // No more Connected Apps checking - that was the anti-pattern
  return <Outlet />;
};
