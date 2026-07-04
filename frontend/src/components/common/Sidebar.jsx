function Sidebar({children}) {
  return (
    <aside className="w-60 m-3 mr-0 rounded-2xl bg-white border border-slate-200 hover:shadow-xl transition-all duration-300">
      <nav className="p-4 space-y-2.5 flex flex-col">
        
        {children}

      </nav>
    </aside>
  );
}

export default Sidebar;