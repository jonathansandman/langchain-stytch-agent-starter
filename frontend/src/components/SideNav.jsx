import { useStytchB2BClient } from '@stytch/react/b2b';
import { useCallback } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { dashboardConsentUrl } from '../utils/stytchConfig';

export const SideNav = () => {
  const stytch = useStytchB2BClient();
  const navigate = useNavigate();
  const handleLogout = useCallback(async () => {
    await stytch.session.revoke();
    navigate('/');
  }, [stytch, navigate]);

  return (
    <nav className="sidebar">
      <div className="nav-links">
        <NavLink
          to={dashboardConsentUrl}
          className={({ isActive }) => (isActive ? 'active-link' : '')}
        >
          Home
        </NavLink>
        <NavLink to="/members" className={({ isActive }) => (isActive ? 'active-link' : '')}>
          Members
        </NavLink>
        <NavLink to="/settings" className={({ isActive }) => (isActive ? 'active-link' : '')}>
          Settings
        </NavLink>
      </div>
      <div className="logout-link" onClick={handleLogout}>
        Log Out
      </div>
    </nav>
  );
};
