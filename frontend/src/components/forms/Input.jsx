import { forwardRef } from "react";

const Input = forwardRef(
  ({ className = "", ...props }, ref) => {
    return (
      <input
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
      />
    );
  }
);

Input.displayName = "Input";

export default Input;