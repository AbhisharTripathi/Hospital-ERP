export function getAccessToken() {
    const authStorage = localStorage.getItem("auth-storage");
    if(!authStorage) return null;

    return JSON.parse(authStorage)?.state?.token ?? null;
}