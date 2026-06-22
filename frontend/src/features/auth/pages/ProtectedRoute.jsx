import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore.js';

function ProtectedRoute({ allowedRoles }) {

  const user = useAuthStore((state) => state.user);
  const isAuthorized = useAuthStore((state) => state.isAuthorized);

  // if(!isAuthorized) {
  //   return <Navigate to="/auth/login" replace />
  // }

  // if(allowedRoles && !allowedRoles.includes(user?.role)) {
  //   return <Navigate to="/unauthorized" replace />
  // }

  return <Outlet />
}

export default ProtectedRoute