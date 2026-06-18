import { useAuthStore } from "@/store/authStore.js"
import { Navigate, Outlet } from "react-router-dom";

function AppAuthWrapper() {

    const isAuthenticated = useAuthStore(state => state.isAuthenticated);

    // if(!isAuthenticated) {
    //     return <Navigate to="/welcome" replace/>
    // }

  return <Outlet />
}

export default AppAuthWrapper