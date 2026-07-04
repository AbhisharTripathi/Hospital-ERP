import { Outlet } from "react-router-dom";

function AuthLayout() {
  return (
      <main className="main-section-wrapper">
        <Outlet />
      </main>
  );
}

export default AuthLayout;