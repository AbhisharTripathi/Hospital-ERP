import { forwardRef } from "react";

const Select = forwardRef(
  ({ children, className = "", ...props }, ref) => {
    return (
      <select
        ref={ref}
        {...props}
        className={`
          w-full
          rounded-lg
          border
          border-slate-300
          px-3
          py-2
          outline-none
          transition
          focus:border-blue-500
          focus:ring-2
          focus:ring-blue-100
          ${className}
        `}
      >
        {children}
      </select>
    );
  }
);

Select.displayName = "Select";

export default Select;