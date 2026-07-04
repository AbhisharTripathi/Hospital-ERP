import { forwardRef } from "react";

const Textarea = forwardRef(
  ({ className = "", ...props }, ref) => {
    return (
      <textarea
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

Textarea.displayName = "Textarea";

export default Textarea;