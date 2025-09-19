import { Route, Routes, useLocation, Navigate } from 'react-router-dom';
import { useStytchMemberSession } from '@stytch/react/b2b';

import { Dashboard } from './components/Dashboard';
import { SideNav } from './components/SideNav';
import { Authenticate } from './components/Authenticate';
import { ProtectedRoutes } from './components/ProtectedRoutes';
import { Members } from './components/Members';
import { Settings } from './components/Settings';
import { ConsentForm } from './components/ConsentForm';
import './App.css';

export const App = () => {
  const location = useLocation();
  const { session } = useStytchMemberSession();
  const showSidebar =
    session && ['/dashboard', '/members', '/settings'].includes(location.pathname);

  return (
    <div className={showSidebar ? 'in-app-container' : 'login-container'}>
      {showSidebar && <SideNav />}
      <div>
        <Routes>
          <Route path="/" element={<Navigate to="/authenticate" replace />} />
          <Route path="/authenticate" element={<Authenticate />} />
          <Route path="/consent" element={<ConsentForm />} />
          <Route element={<ProtectedRoutes />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/members" element={<Members />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Routes>
      </div>
    </div>
  );
};
