import React, { useEffect, useRef, useState } from "react";
import { FaUserCircle, FaSignInAlt, FaSignOutAlt } from "react-icons/fa";
import { Link } from "react-router-dom";

function UserProfileMenu({ user, onLogin, onLogout }) {
  const [open, setOpen] = useState(false);
  const menuRef = useRef(null);

  // Close on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={menuRef}>
      {/* Avatar Button */}
      <button
        onClick={() => setOpen((prev) => !prev)}
        className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 transition"
      >
        <FaUserCircle size={22} />
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute right-0 mt-2 w-60 bg-white border border-slate-200 rounded-xl shadow-lg z-50 overflow-hidden">
          
          {/* User Info */}
          <div className="p-3 border-b border-slate-100 bg-slate-50">
            {user ? (
              <>
                <p className="text-sm font-semibold text-slate-800">
                  {user.role}
                </p>
                <p className="text-xs text-slate-500 truncate">
                  {user.email}
                </p>
              </>
            ) : (
              <p className="text-sm text-slate-500">
                Not logged in
              </p>
            )}
          </div>

          {/* Actions */}
          <div className="p-2">
            {!user ? (
              <Link to="/auth/login"
                onClick={() => {
                  setOpen(false);
                  onLogin?.();
                }}
                className="w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg hover:bg-slate-100"
              >
                <FaSignInAlt className="text-blue-600" />
                Login
              </Link>
            ) : (
              <button
                onClick={() => {
                  setOpen(false);
                  onLogout?.();
                }}
                className="w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg hover:bg-red-50 text-red-600"
              >
                <FaSignOutAlt />
                Logout
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default UserProfileMenu;