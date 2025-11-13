"use client";
import styles from "./Navbar.module.css";
import { Home, Clock, Users, User, LogIn } from "lucide-react";

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <h1 className={styles.logo}>FaceAttend</h1>
      <div className={styles.navLinks}>
        <a href="/dashboard" className={styles.navLink}>
          <Home className={styles.icon} />
          Dashboard
        </a>
        <a href="/history" className={styles.navLink}>
          <Clock className={styles.icon} />
          History
        </a>
        <a href="/students" className={styles.navLink}>
          <Users className={styles.icon} />
          Students
        </a>
        <a href="/profile" className={styles.navLink}>
          <User className={styles.icon} />
          Profile
        </a>
        <a href="/login" className={styles.navLink}>
          <LogIn className={styles.icon} />
          Login
        </a>
      </div>
    </nav>
  );
}
