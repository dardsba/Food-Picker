import { auth, googleProvider } from "./firebase-config.js";
import {
  onAuthStateChanged,
  signInWithPopup,
  signOut
} from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";

const loginButton = document.getElementById("login-google");
const loginLink = document.getElementById("login-link");
const logoutButton = document.getElementById("logout");
const userName = document.getElementById("user-name");
const userAvatar = document.getElementById("user-avatar");

const setLoggedOutUI = () => {
  if (loginButton) loginButton.hidden = false;
  if (loginLink) loginLink.hidden = false;
  if (logoutButton) logoutButton.hidden = true;
  if (userName) userName.textContent = "Guest";
  if (userAvatar) {
    userAvatar.textContent = "U";
    userAvatar.style.backgroundImage = "";
  }
};

const setLoggedInUI = (user) => {
  if (loginButton) loginButton.hidden = true;
  if (loginLink) loginLink.hidden = true;
  if (logoutButton) logoutButton.hidden = false;
  if (userName) userName.textContent = user.displayName || user.email || "User";
  if (userAvatar) {
    if (user.photoURL) {
      userAvatar.textContent = "";
      userAvatar.style.backgroundImage = `url('${user.photoURL}')`;
    } else {
      userAvatar.textContent = (user.displayName || user.email || "U").charAt(0).toUpperCase();
      userAvatar.style.backgroundImage = "";
    }
  }
};

if (loginButton) {
  loginButton.addEventListener("click", async () => {
    try {
      await signInWithPopup(auth, googleProvider);
    } catch (error) {
      console.error("Google sign-in failed", error);
      alert("Google sign-in failed. Check console for details.");
    }
  });
}

if (logoutButton) {
  logoutButton.addEventListener("click", async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Sign out failed", error);
      alert("Sign out failed. Check console for details.");
    }
  });
}

onAuthStateChanged(auth, (user) => {
  if (user) {
    setLoggedInUI(user);
    if (window.location.pathname.endsWith("/login.html")) {
      window.location.href = "index.html";
    }
  } else {
    setLoggedOutUI();
    if (window.location.pathname.endsWith("/index.html") || window.location.pathname.endsWith("/")) {
      window.location.href = "login.html";
    }
  }
});