"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./Auth.module.css";

export default function AuthPage() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ name: "", email: "", password: "" });

  const toggleMode = () => setIsLogin((prev) => !prev);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Skip authentication, navigate directly
    router.push("/dashboard");
  };

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

        <form className={styles.form} onSubmit={handleSubmit}>
          {!isLogin && (
            <div className={styles.inputGroup}>
              <label htmlFor="name">Full Name</label>
              <input
                id="name"
                type="text"
                placeholder="John Doe"
                value={formData.name}
                onChange={handleChange}
              />
            </div>
          )}

          <div className={styles.inputGroup}>
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={formData.email}
              onChange={handleChange}
            />
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
            />
          </div>

          <button type="submit" className="btn w-full mt-3">
            {isLogin ? "Login" : "Register"}
          </button>
        </form>

        <p className={styles.switchText}>
          {isLogin ? "Don’t have an account?" : "Already registered?"}{" "}
          <button
            type="button"
            onClick={toggleMode}
            className={styles.link}
          >
            {isLogin ? "Register" : "Login"}
          </button>
        </p>
      </div>
    </main>
  );
}
