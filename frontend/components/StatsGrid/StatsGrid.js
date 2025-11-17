"use client";

import styles from "@/app/dashboard/dashboard.module.css";
import Donut from "@/components/charts/Donut";
import BarChart from "@/components/charts/BarChart";

export default function StatsGrid() {
  return (
    <section className={styles.statsGrid}>
      <div className={styles.card}>
        <h3>Day wise summary</h3>
        <Donut percent={80} />
      </div>

      <div className={styles.card}>
        <h3>Weekly summary</h3>
        <BarChart
          values={[60, 40, 70, 50, 90, 60, 80]}
        />
      </div>

      <div className={styles.card}>
        <h3>Upcoming class</h3>

        <ul className={styles.upcoming}>
          <li>July 4pm UI/UX designing</li>
          <li>June 9am Graphic designing</li>
          <li>August 5pm Full stack developer</li>
        </ul>
      </div>
    </section>
  );
}
