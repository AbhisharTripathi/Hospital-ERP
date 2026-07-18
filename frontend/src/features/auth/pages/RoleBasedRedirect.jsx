import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore.js';

const RoleBasedRedirect = () => {
  const user = useAuthStore(state => state.user);

  switch (user?.role) {
    case 'DOCTOR':
      return <Navigate to="/doctor" replace />;
    case 'PATIENT':
      return <Navigate to="/patient" replace />;
    case 'RECEPTIONIST':
      return <Navigate to="/receptionist" replace />;
    case "ADMIN":
      return <Navigate to="/admin" replace />;
    case "SUPER_ADMIN":
      return <Navigate to="/admin" replace />;
    default:
      return <Navigate to="/welcome" replace />;
  }
};

export default RoleBasedRedirect;