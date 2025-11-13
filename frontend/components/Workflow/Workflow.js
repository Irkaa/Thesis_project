"use client";

import styles from "./Workflow.module.css";
import { User, School, Camera, Check } from "lucide-react";

const steps = [
  { icon: <User />, title: "Login", desc: "Login securely to your account" },
  { icon: <School />, title: "Select Class", desc: "Select the class you want to take attendance for" },
  { icon: <Camera />, title: "Capture Faces", desc: "Capture student faces with your camera" },
  { icon: <Check />, title: "Record Attendance", desc: "Attendance is recorded automatically" },
];

export default function Workflow() {
  return (
    <section className={styles.workflow}>
      <h2 className={styles.heading}>How It Works</h2>
      <div className={styles.workflowContainer}>
        {steps.map((step, index) => (
          <div key={index} className={styles.stepWrapper}>
            <div className={styles.step}>
              <div className={styles.iconWrapper}>
                <span className={styles.stepNumber}>{index + 1}</span>
                {step.icon}
              </div>
              <div className={styles.stepText}>
                <h3>{step.title}</h3>
                <p>{step.desc}</p>
              </div>
            </div>
            {index < steps.length - 1 && (
              <div className={styles.arrow}>
                <svg viewBox="0 0 60 10">
                  <defs>
                    <marker
                      id="arrowhead"
                      markerWidth="6"
                      markerHeight="6"
                      refX="5"
                      refY="3"
                      orient="auto"
                    >
                      <polygon points="0 0, 6 3, 0 6" fill="#0070f3" />
                    </marker>
                  </defs>
                  <path d="M0,5 L60,5" />
                </svg>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
