"use client";

import styles from "./Hero.module.css";

export default function Hero() {
  return (
    <section className={styles.hero}>
      <div className={styles.content}>
        <h1 className={styles.title}>Smart Attendance System</h1>
        <p className={styles.subtitle}>
          Record and manage student attendance instantly using face recognition.
        </p>
        <div className={styles.buttons}>
          <a href="/login" className="btn">Login</a>
          <a href="/dashboard" className="btn-secondary">Dashboard</a>
        </div>
      </div>
    </section>
  );
}
