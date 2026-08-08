import Sidebar from "@/components/common/Sidebar.jsx";
import SideNavLink from "@/components/common/SideNavLink.jsx";
import { FaUserPlus, FaTachometerAlt, FaPlus } from "react-icons/fa";

function DoctorSidebar() {
  return (

    <Sidebar>
      <SideNavLink link="/doctor"
        label="Dashboard"
        icon={<FaTachometerAlt />}
        end
      />  

      <SideNavLink link="/doctor/appointments"
        label="Appointments"
        icon={<FaUserPlus />}
      />

      <SideNavLink link="/doctor/schedule"
        label="Schedule"
        icon={<FaPlus />}
      />

    </Sidebar>
  );
}

export default DoctorSidebar;