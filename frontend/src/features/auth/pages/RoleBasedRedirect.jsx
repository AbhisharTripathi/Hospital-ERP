import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore.js';

const RoleBasedRedirect = () => {
  const user = useAuthStore(state => state.user);

  switch (user?.role) {
    case 'doctor':
      return <Navigate to="/doctor" replace />;
    case 'patient':
      return <Navigate to="/patient" replace />;
    case 'receptionist':
      return <Navigate to="/receptionist" replace />;
    default:
      return <Navigate to="/welcome" replace />;
  }
};

export default RoleBasedRedirect;