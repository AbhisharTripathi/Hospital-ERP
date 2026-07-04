import AdminSidebar from "../components/AdminSidebar.jsx"
import { Outlet } from "react-router-dom";

export function AdminLayout() {
    return (
    <div className="content-wrapper">
      <AdminSidebar />
      <main className="main-section-wrapper">
        <Outlet />
      </main>
    </div>
    )
}