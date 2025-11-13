"use client";

import Navbar from "@/components/Navbar/Navbar";
import Hero from "@/components/Hero/Hero";
import Features from "@/components/Features/Features";
import Workflow from "@/components/Workflow/Workflow";
import Footer from "@/components/Footer/Footer";

import styles from "@/styles/home/Home.module.css";

export default function Home() {
  return (
    <>
      <Navbar />
      <Hero />
      <Features />
      <Workflow />
      <Footer />
    </>
  );
}
