import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="w-64 border-r">
      <nav className="p-4 space-y-2 flex flex-col">
        <NavLink to="/dashboard">
          Dashboard
        </NavLink>

        <NavLink to="/patients">
          Patients
        </NavLink>

        <NavLink to="/doctors">
          Doctors
        </NavLink>

        <NavLink to="/appointments">
          Appointments
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;