// not needed

import { useEffect } from "react";

import { useAuthStore } from "@/store/authStore";

import { getCurrentUser } from "@/features/auth/api/authApi";

function AuthInitializer() {
  const token = useAuthStore(
    (state) => state.token
  );

  const setUser = useAuthStore(
    (state) => state.setUser
  );

  const logout = useAuthStore(
    (state) => state.logout
  );

  const user = useAuthStore(
    (state) => state.user
  );

  const setIsLoading = useAuthStore(state => state.setIsLoading);

  useEffect(() => {
    const loadUser = async () => {
      if (!token) return;

      try {
        setIsLoading(true);
        console.log("loading true")
        const user = await getCurrentUser();
        setUser(user);

      } catch (error) {
        console.error(error);

        logout();
      } finally {
        setIsLoading(false);
        console.log("loading false")
      }
    };

    loadUser();
  }, [token, setUser, logout]);

  return <div>{user && user.role}</div>;
}

export default AuthInitializer;