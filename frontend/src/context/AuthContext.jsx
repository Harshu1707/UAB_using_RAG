import { createContext, useContext, useMemo, useState } from 'react';
import { login as apiLogin, register as apiRegister } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('uab_user') || 'null'));
  const [token, setToken] = useState(() => localStorage.getItem('uab_token'));

  const persistSession = (data) => {
    localStorage.setItem('uab_token', data.access_token);
    localStorage.setItem('uab_user', JSON.stringify(data.user));
    setToken(data.access_token);
    setUser(data.user);
  };

  const login = async (email, password) => {
    const { data } = await apiLogin(email, password);
    persistSession(data);
  };

  const register = async (payload) => {
    const { data } = await apiRegister(payload);
    persistSession(data);
  };

  const logout = () => {
    localStorage.removeItem('uab_token');
    localStorage.removeItem('uab_user');
    setUser(null);
    setToken(null);
  };

  const value = useMemo(
    () => ({ user, token, isAuthenticated: Boolean(token), login, register, logout }),
    [user, token],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
