import { Outlet } from 'react-router-dom'
import Sidebar from "@/components/layouts/Sidebar";
import ReceptionistSidebar from "@/features/receptionist/components/ReceptionistSidebar.jsx"

function ReceptionistLayout() {

  return (
    <div className="content-wrapper bg-linear-to-br from-white via-sky-50 to-blue-100
    ">
      <ReceptionistSidebar />
      <main className="main-section-wrapper">
        <Outlet />
      </main>
    </div>
  )
 
}

export default ReceptionistLayout