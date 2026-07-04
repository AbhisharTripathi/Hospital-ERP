function SubmitButton({
  isLoading,
  children,
  className = "",
}) {
  return (
    <button
      type="submit"
      disabled={isLoading}
      className={
        `px-6
        py-2
        rounded-lg
        bg-blue-600
        text-white
        font-medium
        hover:bg-blue-700
        disabled:opacity-60
        ${className}`
      }
    >
      {isLoading ? "Submitting..." : children}
    </button>
  );
}

export default SubmitButton;