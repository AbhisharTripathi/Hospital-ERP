import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { getCurrentUser } from "@/features/auth/api/authApi";

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null, 
      token: null, 
      isLoading: false,
      isAuthenticated: false,

      login: ( access_token ) => {

        set({
          token: access_token,
          isAuthenticated: true,
        });
        get().fetchCurrentUser();
      },

      logout: () => {

        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
        console.log("logged out");
      },

      // setUser: (user) => {
      //   set({ user });
      // },

      fetchCurrentUser : async () => {
        const { token, logout } = get();
        if(!token) return;
        set({ isLoading: true});

        try {
          console.log("fetching current user.");
          const user = await getCurrentUser();
          if(user.user_id){
            set({user});
          } else {
            logout();
          }
          
        } catch (err) {
          console.error(err);
          logout();
        } finally {
          set({ isLoading: false});
        }
      }
    }),

    {
      name: "auth-storage",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ token: state.token }),
      onRehydrateStorage: () => {
        console.log("Hydration is starting..."); 

        return (state, error) => {
          if (error) {
            console.error("Failed to read from localStorage!", error);
          } else {
            console.log("Hydration finished perfectly!");
            if (state?.token) state.fetchCurrentUser();
          }
        };
      }
    }
  )
);