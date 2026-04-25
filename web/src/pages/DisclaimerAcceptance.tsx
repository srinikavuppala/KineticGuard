import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import api from '../utils/api';
import { setCredentials } from '../store/slices/authSlice';


export default function DisclaimerAcceptance() {
  const [agreed, setAgreed] = useState(false);
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

      const handleAccept = async () => {
    if (!agreed) return;
    setLoading(true);

    try {
      // Tell backend to save the legal paper trail
      await api.post('/consents/accept');

      // SLAP A STICKY NOTE ON THE BROWSER IMMEDIATELY
      localStorage.setItem('disclaimer_accepted', 'true');

      // (Optional) Update Redux just in case we need it later
      dispatch(setCredentials({
        user: { id: '1', email: 'test@test.com', is_active: true, disclaimer_accepted: true } as any,
        token: localStorage.getItem('token') || ''
      }));

      // Now navigate!
      navigate('/dashboard');
    } catch (err) {
      alert('Failed to accept disclaimer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '700px', margin: '60px auto', padding: '30px', border: '1px solid #ccc', borderRadius: '8px', backgroundColor: 'white' }}>
      <h2>Legal Disclaimer & Terms of Use</h2>
      <div style={{ height: '300px', overflowY: 'scroll', padding: '15px', backgroundColor: '#f8fafc', borderRadius: '4px', marginBottom: '20px', border: '1px solid #e2e8f0' }}>
        <p><strong>FR-1101: Emergency SOS System Acknowledgment</strong></p>
        <p>By using Kinetic Guard, you acknowledge that this application is designed to detect physical gestures and trigger emergency SOS alerts. Due to the nature of AI and sensor-based detection, false triggers may occur.</p>
        <br/>
        <p><strong>1. Accuracy Limitations:</strong> The gesture recognition model is not 100% accurate. Environmental factors, clothing, or sudden movements may trigger an unintended SOS.</p>
        <p><strong>2. Emergency Services:</strong> Kinetic Guard is a supplementary tool. It does not replace official emergency services (e.g., 911). Do not rely solely on this app in life-threatening situations.</p>
        <p><strong>3. Data Collection:</strong> To provide this service, we collect location data (GPS), device sensor data, and timestamps. This data is processed securely to trigger alerts.</p>
        <p><strong>4. Liability:</strong> You agree to hold harmless the developers of Kinetic Guard for any unintended alarms, delays in alert delivery, or failure to detect an emergency gesture.</p>
      </div>

      <label style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px', cursor: 'pointer' }}>
        <input
          type="checkbox"
          checked={agreed}
          onChange={(e) => setAgreed(e.target.checked)}
        />
        <span>I have read and agree to the Kinetic Guard Terms of Use.</span>
      </label>

      <button
        onClick={handleAccept}
        disabled={!agreed || loading}
        style={{
          width: '100%',
          padding: '12px',
          backgroundColor: agreed ? '#22c55e' : '#94a3b8',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          fontSize: '16px',
          cursor: agreed ? 'pointer' : 'not-allowed'
        }}
      >
        {loading ? 'Saving...' : 'Accept & Continue to Dashboard'}
      </button>
    </div>
  );
}