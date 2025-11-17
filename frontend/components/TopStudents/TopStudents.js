"use client";

import styles from "@/app/dashboard/dashboard.module.css";

export default function TopStudents() {
  return (
    <section className={styles.tableCard}>
      <div className={styles.tableHeader}>Top students</div>

      <table className={styles.topTable}>
        <thead>
          <tr>
            <th>No</th>
            <th>Student name</th>
            <th>Course</th>
            <th>Batch</th>
            <th>Percentage</th>
          </tr>
        </thead>

        <tbody>
          {[1, 2, 3, 4, 5].map((n) => (
            <tr key={n}>
              <td>{String(n).padStart(2, "0")}</td>
              <td>Student {n}</td>
              <td>UXUI Design</td>
              <td>July 4pm</td>
              <td className={styles.pct}>100%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
