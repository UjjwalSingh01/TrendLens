import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { 
  signUp, 
  signIn, 
  logOut, 
  onAuthStateChange,
} from '../firebase/firebaseAuth';
import type { User } from 'firebase/auth';

// Define context type
interface AuthContextType {
  currentUser: User | null;
  signup: (email: string, password: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Custom hook with type
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Provider props type
interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Handle user signup
  const signup = async (email: string, password: string): Promise<void> => {
    await signUp(email, password);
  };

  // Handle user login
  const login = async (email: string, password: string): Promise<void> => {
    await signIn(email, password);
  };

  // Handle user logout
  const logout = async (): Promise<void> => {
    await logOut();
  };

  // Subscribe to auth state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChange((user: User | null) => {
      setCurrentUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const value: AuthContextType = {
    currentUser,
    signup,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}