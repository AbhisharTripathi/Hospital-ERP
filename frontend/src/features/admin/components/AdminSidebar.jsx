import Sidebar from "@/components/common/Sidebar.jsx";
import SideNavLink from "@/components/common/SideNavLink.jsx";
import { FaUserPlus, FaTachometerAlt } from "react-icons/fa";

function AdminSidebar() {
  return (

    <Sidebar>
      <SideNavLink link="/admin"
        label="Dashboard"
        icon={<FaTachometerAlt />}
        end
      />  

      <SideNavLink link="/admin/user/register"
        label="Create User"
        icon={<FaUserPlus />}
      />
    </Sidebar>
  );
}

export default AdminSidebar;