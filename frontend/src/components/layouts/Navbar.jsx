import { NavLink, useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/authStore.js"
import { FaStethoscope } from "react-icons/fa";
import UserProfileMenu from "../common/UserProfileMenu";

export default function Navbar() {

  const user = useAuthStore(state => state.user);
  const logout = useAuthStore(state => state.logout);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/auth/login");
  }
  return (
    <header className="h-16 border-b px-6 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="bg-blue-600 text-white p-2 rounded-xl">
          <FaStethoscope size={26} />
        </div>

        <div>
          <h1 className="font-bold text-xl text-slate-800">
            Hospital ERP
          </h1>
          <p className="text-xs text-slate-500">
            Hospital Management System
          </p>
        </div>
      </div>

      <div className="flex gap-6">
        <UserProfileMenu user={user}
          onLogin={() => console.log("Login")}
          onLogout={handleLogout}
        />
        {/* <div className="capitalize">{user && `${user.role.toLowerCase()}'s Account`}</div>
        {user ? 
          <button onClick={handleLogout} className="btn-primary">Logout</button> :
          <NavLink to="/auth/login" className="btn-primary">Login</NavLink>
        } */}
      </div>
    </header>
  );
}