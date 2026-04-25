import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import AlertMarker from './AlertMarker';

interface Props {
  alerts: any[];
}

export default function LeafletAlertMap({ alerts }: Props) {
  // If we have alerts, zoom to the first alert's GPS. Otherwise, default to New York.
  const center: [number, number] = alerts.length > 0 && alerts[0].latitude && alerts[0].longitude
    ? [alerts[0].latitude, alerts[0].longitude]
    : [40.7128, -74.0060];

  return (
    <MapContainer
      center={center}
      zoom={15}
      style={{ height: '100%', width: '100%', borderRadius: '8px' }}
    >
      {/* OpenStreetMap Tiles (The actual map images) */}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* Drop a pin for every alert */}
      {alerts.map((alert) => (
        alert.latitude && alert.longitude ? (
          <Marker key={alert.id} position={[alert.latitude, alert.longitude]}>
            <AlertMarker alert={alert} />
          </Marker>
        ) : null
      ))}
    </MapContainer>
  );
}