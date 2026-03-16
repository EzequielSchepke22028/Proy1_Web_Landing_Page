import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser]       = useState(null);
  const [loading, setLoading] = useState(true); // cargando sesión inicial

  // Al arrancar la app, restaurar sesión si hay token guardado
  useEffect(() => {
    const token    = localStorage.getItem('access_token');
    const savedUser = localStorage.getItem('user');
    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const login = (tokenData) => {
    localStorage.setItem('access_token', tokenData.access_token);
    localStorage.setItem('user', JSON.stringify(tokenData.user));
    setUser(tokenData.user);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  // Refresca datos del usuario desde /users/me
  const refreshUser = async () => {
    try {
      const { data } = await api.get('/users/me');
      localStorage.setItem('user', JSON.stringify(data));
      setUser(data);
    } catch (e) {
      logout();
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook personalizado — uso: const { user, login, logout } = useAuth()
export const useAuth = () => useContext(AuthContext);