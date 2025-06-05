import { initializeApp } from "firebase/app";
import { 
  getAuth, 
} from "firebase/auth";

// Firebase config type
interface FirebaseConfig {
  apiKey: string;
  authDomain: string;
  projectId: string;
  storageBucket: string;
  messagingSenderId: string;
  appId: string;
}

const firebaseConfig: FirebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY!,
  authDomain: process.env.REACT_APP_AUTH_DOMAIN!,
  projectId: process.env.REACT_APP_PROJECT_ID!,
  storageBucket: process.env.REACT_APP_STORAGE_BUCKET!,
  messagingSenderId: process.env.REACT_APP_SENDER_ID!,
  appId: process.env.REACT_APP_APP_ID!
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);