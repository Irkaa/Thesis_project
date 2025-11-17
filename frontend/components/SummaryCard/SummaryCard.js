"use client";
import styles from "@/app/dashboard/dashboard.module.css";

export default function SummaryCard({ title, value }) {
  return (
    <div className={styles.summaryCard}>
      <h4>{title}</h4>
      <div className={styles.summaryValue}>{value}</div>
    </div>
  );
}
