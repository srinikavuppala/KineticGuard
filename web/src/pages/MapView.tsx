import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchAlerts } from '../store/slices/alertsSlice';
import type { RootState } from '../store';
import LeafletAlertMap from '../components/maps/LeafletAlertMap';
// CRITICAL: Import the CSS file we made, otherwise the map breaks!
import '../styles/leaflet-overrides.css';

export default function MapView() {
  const dispatch = useDispatch();
  const { list: alerts, loading } = useSelector((state: RootState) => state.alerts);

  useEffect(() => {
    dispatch(fetchAlerts() as any);
  }, [dispatch]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 140px)' }}>
      <h2>Live SOS Map</h2>
      {loading ? (
        <p>Loading map data...</p>
      ) : (
        <div style={{ flex: 1, border: '1px solid #e2e8f0', marginTop: '10px' }}>
          <LeafletAlertMap alerts={alerts} />
        </div>
      )}
    </div>
  );
}