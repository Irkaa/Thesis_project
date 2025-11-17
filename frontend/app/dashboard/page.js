"use client";

import Sidebar from "@/components/Sidebar/Sidebar";
import Hero from "@/components/Dashboard_hero/Hero";
import StatsGrid from "@/components/StatsGrid/StatsGrid";
import TopStudents from "@/components/TopStudents/TopStudents";
import styles from "./dashboard.module.css"

export default function DashboardPage() {
  return (
    <div className={styles.appRoot}>
      <Sidebar />

      <main className={styles.main}>
        <Hero />
        <StatsGrid />
        <TopStudents />
      </main>
    </div>
  );
}
