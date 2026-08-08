export default function InfoField({ label, value }) {
  return (
    <div>
      <p className="text-sm text-gray-500">
        {label}
      </p>

      <p className="font-medium mt-1">
        {value || "-"}
      </p>
    </div>
  );
}