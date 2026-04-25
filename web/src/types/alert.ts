export type TriggerMethod = "GESTURE" | "SHAKE" | "POWER_BUTTON" | "TIMEOUT" | "MANUAL";

export type GestureProfile = "DEFAULT" | "HEALTHCARE" | "TEACHER" | "DELIVERY" | "CORPORATE" | "ELDERLY"; // NEW

export interface Alert {
  id: string;
  user_id: string;
  trigger_method: TriggerMethod;
  gesture_profile: GestureProfile; // NEW
  model_version: string | null;
  status: "ACTIVE" | "RESOLVED" | "FALSE_ALARM";
  latitude: number | null;
  longitude: number | null;
  location_address: string | null;
  created_at: string;
}