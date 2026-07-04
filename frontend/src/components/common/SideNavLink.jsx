import { NavLink } from "react-router-dom";

export default function SideNavLink({link, label, icon, end = false}) {
  return (
    <NavLink to={link}
      end={end}
      className={({isActive}) => (
        `py-2.5 pl-5 rounded-2xl font-semibold flex items-center gap-3 ${
        isActive 
          ? "bg-blue-600 text-white hover:bg-blue-700" 
          : " bg-slate-100 text-black hover:bg-slate-200"}`
      )}
    >
      {icon}{label}
    </NavLink>
  )
}