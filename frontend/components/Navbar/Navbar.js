"use client";

import { useEffect, useState } from "react";
import styles from "./Navbar.module.css";
import { Home, Clock, Users, User, LogIn, LogOut } from "lucide-react";
import { isAuthenticated, logout } from "../../utils/auth";

export default function Navbar() {
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    setLoggedIn(isAuthenticated());
  }, []);

  return (
    <nav className={styles.navbar}>
      <h1 className={styles.logo}>FaceAttend</h1>
      <div className={styles.navLinks}>
        <a href="/" className={styles.navLink}>
          <Home className={styles.icon} />
          Home
        </a>

        {loggedIn && (
          <>
            <a href="/dashboard" className={styles.navLink}>
              <Users className={styles.icon} />
              Dashboard
            </a>
            <a href="/history" className={styles.navLink}>
              <Clock className={styles.icon} />
              History
            </a>
            <a href="/profile" className={styles.navLink}>
              <User className={styles.icon} />
              Profile
            </a>
          </>
        )}

        {!loggedIn ? (
          <a href="/auth" className={styles.navLink}>
            <LogIn className={styles.icon} />
            Login
          </a>
        ) : (
          <button onClick={logout} className={styles.navLink}>
            <LogOut className={styles.icon} />
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}
