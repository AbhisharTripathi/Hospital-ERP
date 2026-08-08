import DoctorSidebar from "../components/DoctorSidebar.jsx"
import { Outlet } from "react-router-dom";

export default function DoctorLayout() {
    return (
    <div className="content-wrapper">
      <DoctorSidebar />
      <main className="main-section-wrapper">
        <Outlet />
      </main>
    </div>
    )
}