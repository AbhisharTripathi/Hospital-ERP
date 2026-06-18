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

  useEffect(() => {
    const loadUser = async () => {
      if (!token) return;

      try {

        const user = await getCurrentUser();
        setUser(user);

      } catch (error) {
        console.error(error);

        logout();
      }
    };

    loadUser();
  }, [token, setUser, logout]);

  return null;
}

export default AuthInitializer;