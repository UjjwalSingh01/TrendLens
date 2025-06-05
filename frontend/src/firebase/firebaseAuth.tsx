import {
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  type UserCredential,
  type User
} from "firebase/auth";
import { auth } from "./firebaseConfig";

// Authentication functions
export const signUp = (email: string, password: string): Promise<UserCredential> => {
  return createUserWithEmailAndPassword(auth, email, password);
};

export const signIn = (email: string, password: string): Promise<UserCredential> => {
  return signInWithEmailAndPassword(auth, email, password);
};

export const logOut = (): Promise<void> => signOut(auth);

// Auth state observer with types
export const onAuthStateChange = (callback: (user: User | null) => void) => {
  return onAuthStateChanged(auth, callback);
};