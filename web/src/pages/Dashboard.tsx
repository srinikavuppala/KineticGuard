import { useSelector } from 'react-redux';
import type { RootState } from '../store';

export default function Dashboard() {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);

  if (!isAuthenticated) {
    return <h1>Please log in.</h1>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Welcome to the Kinetic Guard Dashboard 🛡️</h1>
      <p>You are successfully logged into the system!</p>
    </div>
  );
}