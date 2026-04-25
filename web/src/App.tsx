import { Routes, Route, Navigate, Outlet } from 'react-router-dom'; // <-- ADDED Outlet
import ProtectedRoute from './components/common/ProtectedRoute';
import AppLayout from './components/layout/AppLayout';
import Login from './pages/Login';
import DisclaimerAcceptance from './pages/DisclaimerAcceptance';
import Dashboard from './pages/Dashboard';
import AlertList from './pages/AlertList';
import MapView from './pages/MapView';
import NotFound from './pages/NotFound';

// The Bouncer Component - FIXED TO USE OUTLET!
function DisclaimerGate() {
  const disclaimerAccepted = localStorage.getItem('disclaimer_accepted') === 'true';

  if (!disclaimerAccepted) {
    return <Navigate to="/disclaimer" replace />;
  }

  // This is where the child routes (Dashboard, Alerts) render in React Router!
  return <Outlet />;
}

export default function App() {
  return (
    <Routes>
      {/* Public Route */}
      <Route path="/login" element={<Login />} />
      <Route path="/disclaimer" element={<DisclaimerAcceptance />} />

      {/* Protected Routes inside the App Frame */}
      <Route element={<ProtectedRoute />}>
        {/* If they haven't signed, force them to /disclaimer */}
        <Route element={<DisclaimerGate />}>
          <Route element={<AppLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/alerts" element={<AlertList />} />
            <Route path="/map" element={<MapView />} />
          </Route>
        </Route>
      </Route>

      {/* Fallbacks */}
      <Route path="*" element={<NotFound />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}