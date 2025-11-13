"use client";

import { useState } from "react";
import styles from "./Auth.module.css";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  const toggleMode = () => setIsLogin((prev) => !prev);

  return (
    <main className={styles.container}>
      <div className={styles.card}>
        <h1 className={styles.title}>
          {isLogin ? "Welcome Back" : "Create Account"}
        </h1>
        <p className={styles.subtitle}>
          {isLogin
            ? "Sign in to manage attendance and view reports."
            : "Register as a teacher to start managing attendance."}
        </p>

        <form className={styles.form}>
          {!isLogin && (
            <div className={styles.inputGroup}>
              <label htmlFor="name">Full Name</label>
              <input id="name" type="text" placeholder="John Doe" required />
            </div>
          )}

          <div className={styles.inputGroup}>
            <label htmlFor="email">Email Address</label>
            <input id="email" type="email" placeholder="you@example.com" required />
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="password">Password</label>
            <input id="password" type="password" placeholder="••••••••" required />
          </div>

          <button type="submit" className="btn w-full mt-3">
            {isLogin ? "Login" : "Register"}
          </button>
        </form>

        <p className={styles.switchText}>
          {isLogin ? "Don’t have an account?" : "Already registered?"}{" "}
          <span onClick={toggleMode} className={styles.link}>
            {isLogin ? "Register" : "Login"}
          </span>
        </p>
      </div>
    </main>
  );
}
