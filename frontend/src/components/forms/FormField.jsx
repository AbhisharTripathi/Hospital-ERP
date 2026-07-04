import FormError from "./FormError.jsx";

function FormField({
  label,
  required = false,
  error,
  children,
}) {
  return (
    <div className="space-y-1">
      <label className="block text-sm font-medium text-slate-700">
        {label}

        {required && (
          <span className="text-red-500 ml-1">
            *
          </span>
        )}
      </label>

      {children}

      <FormError error={error} />
    </div>
  );
}

export default FormField;