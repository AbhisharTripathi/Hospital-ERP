import { Outlet } from "react-router-dom";

import Sidebar from "@/components/layouts/Sidebar";
import Navbar from "@/components/layouts/Navbar";

function AppLayout() {
  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <Navbar />

      <div className="flex flex-row flex-1 min-h-0">
        <Sidebar />
        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default AppLayout;