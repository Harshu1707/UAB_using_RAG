export default function AnalyticsCard({ title, value, caption }) {
  return (
    <div className="glass rounded-2xl p-5">
      <p className="text-sm opacity-70">{title}</p>
      <h3 className="mt-2 text-3xl font-bold">{value}</h3>
      <p className="text-sm opacity-70">{caption}</p>
    </div>
  );
}
