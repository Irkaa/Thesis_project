"use client";

import style from "@/styles/home/Home.module.css";
import { useEffect, useState } from "react";
import { fetchAPI } from "../utils/api";

export default function Home() {
  const [apiMessage, setApiMessage] = useState("Loading...");

  useEffect(() => {
    async function getData() {
      const data = await fetchAPI("/");
      setApiMessage(data ? data.message : "Backend not reachable");
    }
    getData();
  }, []);

  return (
    <main >
      <h1 className={style.h1}>Student Attendance System</h1>
      <p>Backend connection test:</p>
      <p>{apiMessage}</p>
    </main>
  );
}
