import { NavLink } from 'react-router-dom';

const navItems = [
  { path: '/dashboard', label: 'Dashboard 🏠' },
  { path: '/alerts', label: 'SOS Alerts 🚨' },
  { path: '/map', label: 'Live Map 🗺️' },
];

export default function Sidebar() {
  return (
    <div style={{
      width: '250px',
      minHeight: '100vh',
      backgroundColor: '#1e293b',
      color: 'white',
      padding: '20px 0',
      display: 'flex',
      flexDirection: 'column'
    }}>
      <h2 style={{ padding: '0 20px 20px', borderBottom: '1px solid #334155' }}>
        Kinetic Guard
      </h2>
      <nav style={{ display: 'flex', flexDirection: 'column', gap: '5px', padding: '10px' }}>
        {navItems.map((item) => (
                    <NavLink
            key={item.path}  /* <-- ADD THIS LINE */
            to={item.path}
            style={({ isActive }) => ({
              padding: '10px 20px',
              borderRadius: '5px',
              textDecoration: 'none',
              color: 'white',
              backgroundColor: isActive ? '#3b82f6' : 'transparent',
            })}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}