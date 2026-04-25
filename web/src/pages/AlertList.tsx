import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchAlerts } from '../store/slices/alertsSlice';
import { useAlertsWebSocket } from '../hooks/useAlertsWebSocket';
import type { RootState, AppDispatch } from '../store';

const formatTrigger = (method: string) => {
  const map: Record<string, string> = {
    "INDEX_UP": "1 Finger ☝️", "MIDDLE_UP": "1 Finger ☝️", "RING_UP": "1 Finger ☝️", "PINKY_UP": "1 Finger 🤙", "ONE_FINGER_UP": "1 Finger ☝️",
    "THUMB_UP": "Thumb Up 👍", "THUMB_DOWN": "Thumb Down 👎",
    "INDEX_MIDDLE_UP": "2 Fingers ✌️", "INDEX_RING_UP": "2 Fingers ✌️", "INDEX_PINKY_UP": "2 Fingers ✌️", "MIDDLE_RING_UP": "2 Fingers ✌️", "MIDDLE_PINKY_UP": "2 Fingers ✌️", "RING_PINKY_UP": "2 Fingers ✌️", "THUMB_INDEX_UP": "2 Fingers 🤞", "THUMB_PINKY_UP": "2 Fingers 🤞", "TWO_FINGERS_UP": "2 Fingers ✌️",
    "INDEX_MIDDLE_RING_UP": "3 Fingers 🤟", "INDEX_MIDDLE_PINKY_UP": "3 Fingers 🤟", "INDEX_RING_PINKY_UP": "3 Fingers 🤟", "MIDDLE_RING_PINKY_UP": "3 Fingers 🤟", "THREE_FINGERS_UP": "3 Fingers 🤟",
    "FOUR_FINGERS_UP": "4 Fingers 🖐️", "ALL_FIVE_UP": "5 Fingers ✋",
    "GESTURE": "Hand Detected ✋", "SHAKE": "Phone Shaken 📳", "POWER_BUTTON": "Power Button 🔘", "TIMEOUT": "Session Timeout ⏱️", "MANUAL": "Manual Trigger 🆘"
  };
  return map[method] || method;
};

export default function AlertList() {
  const dispatch = useDispatch<AppDispatch>();
  const { list: alerts, loading, error } = useSelector((state: RootState) => state.alerts);

  useAlertsWebSocket();

  useEffect(() => {
    dispatch(fetchAlerts());
  }, [dispatch]);

  return (
    <div style={{
      backgroundColor: '#0f172a', // Deep Midnight Blue (The industry standard for ops centers)
      minHeight: '100vh',
      padding: '30px',
      fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    }}>

      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '30px',
        paddingBottom: '15px',
        borderBottom: '1px solid rgba(148, 163, 184, 0.1)' // Very subtle bottom line
      }}>
        <h2 style={{ color: '#f1f5f9', fontSize: '26px', fontWeight: '700', margin: 0 }}>
          🛡️ Live Secure Feed
        </h2>
        <div style={{
          padding: '6px 14px',
          backgroundColor: 'rgba(239, 68, 68, 0.15)', // Soft dark-red background
          color: '#fca5a5',
          borderRadius: '20px',
          fontSize: '13px',
          fontWeight: '600',
          border: '1px solid rgba(239, 68, 68, 0.2)'
        }}>
          {alerts.filter(a => a.status === 'ACTIVE').length} Active Threats
        </div>
      </div>

      {loading ? (
        <p style={{color: '#64748b', textAlign: 'center', marginTop: '50px'}}>Syncing secure channels...</p>
      ) : error ? (
        <p style={{color: '#f87171', textAlign: 'center', marginTop: '50px'}}>{error}</p>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(380px, 1fr))',
          gap: '16px'
        }}>
          {alerts.map((alert) => (
            /* THE PERFECT OPS CARD */
            <div key={alert.id} style={{
              backgroundColor: '#1e293b', // Slate 800 - Dark enough to blend, light enough to stand out
              borderRadius: '12px',
              padding: '20px',
              // Precise left accent line (Professional Blue, not harsh Red)
              borderLeft: '3px solid #3b82f6',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3)'
            }}>

              {/* Top Row */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <span style={{ color: '#64748b', fontSize: '12px', fontFamily: 'monospace', fontWeight: '500', letterSpacing: '0.5px' }}>
                  ID: {alert.id.substring(0, 8)}...
                </span>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <span style={{
                    padding: '4px 10px',
                    borderRadius: '6px',
                    fontSize: '12px',
                    fontWeight: '600',
                    backgroundColor: 'rgba(96, 165, 250, 0.15)', // Soft glowing blue
                    color: '#93c5fd'
                  }}>
                    {formatTrigger(alert.trigger_method)}
                  </span>
                  {alert.gesture_profile && alert.gesture_profile !== 'DEFAULT' && (
                    <span style={{
                      padding: '4px 10px',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '600',
                      backgroundColor: 'rgba(52, 211, 153, 0.15)', // Soft glowing green
                      color: '#6ee7b7'
                    }}>
                      {alert.gesture_profile}
                    </span>
                  )}
                </div>
              </div>

              {/* Location */}
              <div style={{ marginBottom: '16px' }}>
                <p style={{ color: '#cbd5e1', fontSize: '14px', margin: 0, lineHeight: '1.5' }}>
                  📍 {alert.location_address || 'Location unavailable'}
                </p>
              </div>

              {/* Bottom Row */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                borderTop: '1px solid rgba(148, 163, 184, 0.1)',
                paddingTop: '12px'
              }}>
                <span style={{ color: '#64748b', fontSize: '12px' }}>
                  🕐 {alert.created_at ? new Date(alert.created_at).toLocaleString() : 'Time not recorded'}
                </span>

                {/* Status Indicator */}
                <span style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  fontSize: '11px',
                  fontWeight: '700',
                  color: '#f87171',
                  textTransform: 'uppercase',
                  letterSpacing: '0.5px'
                }}>
                  <span style={{
                    height: '6px',
                    width: '6px',
                    backgroundColor: '#ef4444',
                    borderRadius: '50%',
                    boxShadow: '0 0 8px rgba(239, 68, 68, 0.6)' // Glowing red dot
                  }}></span>
                  Active
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}