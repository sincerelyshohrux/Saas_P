import React from "react";
import ReactDOM from "react-dom/client";
import { AppProviders } from "@/app/providers";
import { bootstrapAuth } from "@/features/auth/bootstrap";
import { Spinner } from "@/shared/ui/Spinner";
import "@/index.css";

// Saqlangan dark/light rejimni sahifa ochilishidayoq qo'llaymiz
if (localStorage.getItem("theme") === "dark") document.documentElement.classList.add("dark");

function Root() {
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => { let active = true; void bootstrapAuth().finally(() => { if (active) setReady(true); }); return () => { active = false; }; }, []);
  if (!ready) return <div className="grid min-h-screen place-items-center"><Spinner label="Ilova yuklanmoqda" /></div>;
  return <AppProviders />;
}

ReactDOM.createRoot(document.getElementById("root")!).render(<React.StrictMode><Root /></React.StrictMode>);
