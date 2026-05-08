import { useEffect, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import AnalyticsCard from '../components/AnalyticsCard';
import { getAnalytics } from '../services/api';

const COLORS = ['#4f46e5', '#06b6d4', '#22c55e', '#f59e0b', '#ef4444'];

function Chart({ title, children }) {
  return (
    <div className="glass h-80 rounded-3xl p-5">
      <h3 className="mb-4 text-xl font-bold">{title}</h3>
      <ResponsiveContainer width="100%" height="85%">
        {children}
      </ResponsiveContainer>
    </div>
  );
}

export default function AnalyticsDashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getAnalytics().then(setData);
  }, []);

  if (!data) {
    return <div className="p-6">Loading analytics...</div>;
  }

  const totalStudents = data.dist.reduce((total, band) => total + band.count, 0);

  return (
    <div className="space-y-6 p-6">
      <div className="grid gap-4 md:grid-cols-3">
        <AnalyticsCard title="Departments" value={data.cgpa.length} caption="Tracked in SQLite" />
        <AnalyticsCard title="At-risk" value={data.risk.length} caption="Low CGPA or attendance" />
        <AnalyticsCard title="Students" value={totalStudents} caption="Included in CGPA bands" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Chart title="Department-wise CGPA">
          <BarChart data={data.cgpa}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="department" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="average_cgpa" fill="#4f46e5" />
          </BarChart>
        </Chart>

        <Chart title="Pass percentage">
          <LineChart data={data.pass}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="department" />
            <YAxis />
            <Tooltip />
            <Line dataKey="pass_rate" stroke="#22c55e" strokeWidth={3} />
          </LineChart>
        </Chart>

        <Chart title="CGPA distribution">
          <PieChart>
            <Pie data={data.dist} dataKey="count" nameKey="band" label>
              {data.dist.map((_, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </Chart>

        <div className="glass rounded-3xl p-5">
          <h3 className="mb-4 text-xl font-bold">Risk analysis</h3>
          {data.risk.map((student) => (
            <div
              key={student.StudentID}
              className="mb-2 rounded-xl bg-red-50 p-3 text-red-900 dark:bg-red-950 dark:text-red-100"
            >
              {student.Name} — {student.Department}, CGPA {student.CGPA}, Attendance {student.Attendance}%
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
