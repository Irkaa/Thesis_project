"use client";
import styles from "@/app/dashboard/dashboard.module.css";

export default function Donut({ percent }) {
  return (
    <div className={styles.donutPlaceholder}>
      {percent}% donut chart
    </div>
  );
}
