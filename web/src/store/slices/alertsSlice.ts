import { createSlice, createAsyncThunk, type PayloadAction } from '@reduxjs/toolkit';
import api from '../../utils/api';
import type { Alert } from '../../types/alert';

// Keep your fetch for initial load
export const fetchAlerts = createAsyncThunk(
  'alerts/fetchAlerts',
  async () => {
    const response = await api.get('/alerts');
    return response.data;
  }
);

interface AlertState {
  list: Alert[];
  loading: boolean;
  error: string | null;
}

const initialState: AlertState = {
  list: [],
  loading: false,
  error: null,
};

const alertSlice = createSlice({
  name: 'alerts',
  initialState,
  reducers: {
    // NEW: Action specifically for WebSockets
    addWebSocketAlert: (state, action: PayloadAction<Alert>) => {
      // Prevent duplicates just in case
      if (!state.list.find(a => a.id === action.payload.id)) {
        state.list.unshift(action.payload); // Add to the VERY TOP instantly!
      }
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAlerts.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchAlerts.fulfilled, (state, action: PayloadAction<Alert[]>) => {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchAlerts.rejected, (state) => {
        state.loading = false;
        state.error = 'Failed to load alerts';
      });
  },
});

// Export the new action
export const { addWebSocketAlert } = alertSlice.actions;
export default alertSlice.reducer;