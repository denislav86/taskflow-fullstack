import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { authService } from '@/services';
import { useAuthStore } from '@/store';
import type { LoginCredentials, RegisterData } from '@/types';

export function useLogin() {
  const navigate = useNavigate();
  const { setTokens, setUser } = useAuthStore();

  return useMutation({
    mutationFn: async (credentials: LoginCredentials) => {
      const tokens = await authService.login(credentials);
      return tokens;
    },
    onSuccess: (data) => {
      setTokens(data.access_token, data.refresh_token);
      // We don't have a me endpoint, so we'll just set minimal user info
      setUser({
        id: 0, // Will be populated from token claims if needed
        email: '',
        full_name: null,
        is_active: true,
        created_at: new Date().toISOString(),
      });
      toast.success('Welcome back!');
      navigate('/dashboard');
    },
    onError: () => {
      toast.error('Invalid email or password');
    },
  });
}

export function useRegister() {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: async (data: RegisterData) => {
      const user = await authService.register(data);
      return user;
    },
    onSuccess: () => {
      toast.success('Account created! Please log in.');
      navigate('/login');
    },
    onError: (error: Error & { response?: { data?: { detail?: string } } }) => {
      const message = error.response?.data?.detail || 'Registration failed';
      toast.error(message);
    },
  });
}

export function useLogout() {
  const navigate = useNavigate();
  const { logout } = useAuthStore();

  return () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/login');
  };
}

