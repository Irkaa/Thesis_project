"use client";
import styles from "./Footer.module.css";
import { Mail, Linkedin, Github } from "lucide-react";

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        {/* Column 1: Brand */}
        <div className={styles.column}>
          <h2 className={styles.logo}>FaceAttend</h2>
          <p>Automatic face recognition attendance system.</p>
        </div>

        {/* Column 2: Quick Links */}
        <div className={styles.column}>
          <h3>Quick Links</h3>
          <a href="/dashboard" className={styles.link}>Dashboard</a>
          <a href="/history" className={styles.link}>History</a>
          <a href="/students" className={styles.link}>Students</a>
          <a href="/profile" className={styles.link}>Profile</a>
        </div>

        {/* Column 3: Contact / Social */}
        <div className={styles.column}>
          <h3>Contact</h3>
          <a href="mailto:support@faceattend.com" className={styles.link}>
            <Mail className={styles.icon} /> support@faceattend.com
          </a>
          <div className={styles.social}>
            <a href="https://linkedin.com" target="_blank" className={styles.link}>
              <Linkedin className={styles.icon} /> LinkedIn
            </a>
            <a href="https://github.com" target="_blank" className={styles.link}>
              <Github className={styles.icon} /> GitHub
            </a>
          </div>
        </div>
      </div>

      <div className={styles.copy}>
        &copy; {new Date().getFullYear()} FaceAttend. All rights reserved.
      </div>
    </footer>
  );
}
