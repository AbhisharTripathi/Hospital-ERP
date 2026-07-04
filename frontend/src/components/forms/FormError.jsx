function FormError({ error }) {
  if (!error) return null;

  return (
    <p className="mt-1 text-sm text-red-500">
      {error.message}
    </p>
  );
}

export default FormError;