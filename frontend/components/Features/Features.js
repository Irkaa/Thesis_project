"use client";
import { CheckCircle } from "lucide-react"; // lightweight icon library
import styles from "./Features.module.css";

export default function Features() {
  const features = [
    {
      title: "Face Recognition Attendance",
      desc: "Automatically recognize students and mark attendance instantly with precision.",
    },
    {
      title: "Fast & Accurate",
      desc: "AI-powered recognition ensures reliable results for every session.",
    },
    {
      title: "Attendance History & Reports",
      desc: "Easily view detailed attendance logs and export class reports.",
    },
  ];

  return (
    <section className={styles.features}>
      <div className="text-center">
        <h2 className={styles.sectionTitle}>Key Features</h2>
        <p className={styles.sectionSubtitle}>
          Streamline attendance management with intelligent automation.
        </p>
      </div>

      <div className={styles.featureGrid}>
        {features.map((feature, index) => (
          <div key={index} className={styles.featureCard}>
            <CheckCircle className={styles.icon} size={32} />
            <h3>{feature.title}</h3>
            <p>{feature.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
