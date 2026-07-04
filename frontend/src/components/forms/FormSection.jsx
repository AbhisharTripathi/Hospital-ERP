function FormSection({
  title,
  children,
}) {
  return (
    <div className="border rounded-xl p-5 bg-slate-50">
      <h3 className="font-semibold text-slate-800 mb-4">
        {title}
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {children}
      </div>
    </div>
  );
}

export default FormSection;