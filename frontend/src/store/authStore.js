import { create } from "zustand";
import { 
    // setLocalUser,
    // getLocalUser,
    // removeLocalUser,
    setToken,
    getToken,
    removeToken
} from "../utils/localStorageUtils";


export const useAuthStore = create((set) => ({
  user: null, //getInitialUser()
  isLoading: true,
  token: getToken(),
  isAuthenticated: !!getToken(),

  login: ( access_token ) => {
    setToken(access_token);

    // setLocalUser(user);

    set({
    //   user,
      token: access_token,
      isAuthenticated: true,
    });
  },

  logout: () => {
    removeToken();

    // removeLocalUser();

    set({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  },

  setUser: (user) => {
    // setLocalUser(user);

    set({ user });
  },

  setIsLoading: (value) => set({isLoading: value}),
}));