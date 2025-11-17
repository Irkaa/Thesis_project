"use client";
import styles from "@/app/dashboard/dashboard.module.css";

export default function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <div className={styles.brand}>📷 Present Sir</div>

      <nav className={styles.nav}>
        <div className={styles.navItemActive}>Dashboard</div>
        <div className={styles.navItem}>Courses</div>
        <div className={styles.navItem}>Attendances</div>
        <div className={styles.navItem}>Report</div>
        <div className={styles.navItem}>Calendar</div>
      </nav>
    </aside>
  );
}
