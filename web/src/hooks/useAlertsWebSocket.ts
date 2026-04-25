import { useEffect, useRef } from 'react';
import { useDispatch } from 'react-redux';
import { addWebSocketAlert } from '../store/slices/alertsSlice';
import type { Alert } from '../types/alert';

export const useAlertsWebSocket = () => {
  const dispatch = useDispatch();
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    let reconnectTimeout: ReturnType<typeof setTimeout>;

    const connect = () => {
      ws.current = new WebSocket('ws://127.0.0.1:8000/api/v1/ws/alerts');

      ws.current.onopen = () => {
        console.log('✅ WebSocket Connected! Waiting for live alerts...');
      };

      ws.current.onmessage = (event) => {
        try {
          const newAlert: Alert = JSON.parse(event.data);
          console.log('🚨 LIVE ALERT RECEIVED VIA WEBSOCKET:', newAlert.trigger_method);
          dispatch(addWebSocketAlert(newAlert));
        } catch (e) {
          console.error("Failed to parse WebSocket message", e);
        }
      };

      ws.current.onclose = () => {
        console.log('❌ WebSocket Disconnected. Reconnecting in 3 seconds...');
        // Reconnect smoothly without reloading the page
        reconnectTimeout = setTimeout(connect, 3000);
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket Error:', error);
        ws.current?.close(); // Trigger the onclose to start the reconnect timer
      };
    };

    connect();

    // Cleanup on unmount (only when leaving the page entirely)
    return () => {
      clearTimeout(reconnectTimeout);
      if (ws.current) {
        ws.current.onclose = null; // Prevent the reconnect loop when intentionally closing
        ws.current.close();
      }
    };
  }, [dispatch]);
};