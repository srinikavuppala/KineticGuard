import { Popup } from 'react-leaflet';
import TriggerMethodBadge from '../alerts/TriggerMethodBadge';

interface Props {
  alert: {
    id: string;
    trigger_method: string;
    location_address: string | null;
    status: string;
    created_at: string;
  };
}

export default function AlertMarker({ alert }: Props) {
  return (
    <Popup>
      <div style={{ padding: '5px' }}>
        <strong>SOS Alert</strong><br />
        <TriggerMethodBadge method={alert.trigger_method} /><br />
        <span style={{ fontSize: '12px' }}>📍 {alert.location_address || 'Unknown'}</span><br />
        <span style={{ fontWeight: 'bold', color: alert.status === 'ACTIVE' ? 'red' : 'green' }}>
          {alert.status}
        </span>
      </div>
    </Popup>
  );
}