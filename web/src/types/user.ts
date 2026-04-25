export interface User {
  id: string;
  email: string;
  is_active: boolean;
  disclaimer_accepted: boolean;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
}