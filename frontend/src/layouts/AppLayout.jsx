import { Outlet } from "react-router-dom";
import Navbar from "@/components/layouts/Navbar.jsx";
import { useAuthStore } from "@/store/authStore.js";

function AppLayout() {

  const isLoading = useAuthStore(state => state.isLoading);

  if(isLoading) {
    return <div>Loading...</div>
  }


  return (
    <div className="flex flex-col h-screen overflow-hidden">

      <Navbar />

      <Outlet />

    </div>
  );
}

export default AppLayout;