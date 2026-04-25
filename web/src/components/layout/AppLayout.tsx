import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function AppLayout() {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Header />
        <main style={{ padding: '20px', backgroundColor: '#f8fafc', flex: 1 }}>
          {/* This is where the actual page content (Dashboard, Alerts) renders */}
          <Outlet />
        </main>
      </div>
    </div>
  );
}