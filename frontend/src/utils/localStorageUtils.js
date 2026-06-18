export const getToken = () =>
  localStorage.getItem("access_token");

export const setToken = (token) =>
  localStorage.setItem(
    "access_token",
    token
  );

export const removeToken = () =>
  localStorage.removeItem(
    "access_token"
  );

export const setLocalUser = (user) => {
    localStorage.setItem(
        "user",
        JSON.stringify(user)
    );
};

export const getLocalUser = () => {
    const user = localStorage.getItem(
        "user"
    );
    return JSON.parse(user);
}

export const removeLocalUser = () => {
    localStorage.removeItem("user");
}