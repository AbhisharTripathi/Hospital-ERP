import { useEffect } from "react";
import { useAuthStore } from "@/store/authStore.js"
import { Navigate, Outlet } from "react-router-dom";
import { getCurrentUser } from "@/features/auth/api/authApi";

function AppAuthWrapper() {

    const isAuthenticated = useAuthStore(state => state.isAuthenticated);

    const isLoading = useAuthStore(state => state.isLoading);

    const token = useAuthStore((state) => state.token);

    const setUser = useAuthStore((state) => state.setUser);

    const logout = useAuthStore((state) => state.logout);

    const user = useAuthStore((state) => state.user);

    const setIsLoading = useAuthStore(state => state.setIsLoading);

    useEffect(() => {
      const loadUser = async () => {
        if (!token) {
          setIsLoading(false);
          return;
        }

        try {
          setIsLoading(true); //already true but making sure.
          const user = await getCurrentUser();
          setUser(user);

        } catch (error) {
          console.error(error);

          logout();
        } finally {
          setIsLoading(false);
        }
      };

      loadUser();
    }, [token, setUser, logout]);


    if(isLoading) {
      return <div>Loading...</div>
    }

    // if(!isAuthenticated) {
    //     return <Navigate to="/welcome" replace/>
    // }

  return (
    <Outlet />
  )
}

export default AppAuthWrapper