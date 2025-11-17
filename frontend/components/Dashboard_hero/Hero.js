"use client";

import styles from "@/app/dashboard/dashboard.module.css";
import SummaryCard from "@/components/SummaryCard/SummaryCard";

export default function Hero() {
  return (
    <section className={styles.hero}>
      <div>
        <h2>Our courses</h2>
        <p className={styles.muted}>Number of students in each course</p>
      </div>

      <div className={styles.heroCards}>
        <SummaryCard title="Full stack developer" value="66 Students" />
        <SummaryCard title="UX/UI Designing" value="39 Students" />
        <SummaryCard title="Graphic designing" value="29 Students" />
        <SummaryCard title="Content creator" value="50 Students" />
      </div>
    </section>
  );
}
