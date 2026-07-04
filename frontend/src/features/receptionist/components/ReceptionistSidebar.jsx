import SideNavLink from "@/components/common/SideNavLink.jsx";
import Sidebar from "@/components/common/Sidebar.jsx";
import { FaUserPlus,
  FaUsers,
  FaTachometerAlt
} from "react-icons/fa";

function ReceptionistSidebar() {
  return (
    <Sidebar>
      <SideNavLink link="/receptionist"
          label="Dashboard"
          icon={<FaTachometerAlt />}
          end
        />

        <SideNavLink link="/receptionist/patients/create"
          label="Create Patient"
          icon={<FaUserPlus />}
        />

        <SideNavLink link="/receptionist/patients"
          label="Patients"
          icon={<FaUsers />}
          end
        />
    </Sidebar>
  );
}

export default ReceptionistSidebar;