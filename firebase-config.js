// Firebase modular SDK via CDN for plain HTML usage
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-analytics.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDeC0RmbogfnmdoCTxqasIFYSVtLYSOM6o",
  authDomain: "recipecloud.firebaseapp.com",
  projectId: "recipecloud",
  storageBucket: "recipecloud.firebasestorage.app",
  messagingSenderId: "673470705274",
  appId: "1:673470705274:web:0eb435c3ff81fbbc9195c3",
  measurementId: "G-24MD8Z4MJ6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { app, auth, googleProvider };