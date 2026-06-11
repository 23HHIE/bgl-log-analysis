import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "rechart";

function LiveFeed({ logs }) {
  const chartData = logs.filter((_, i) => ({ index: i * 10, total: i * 10 }));

  return (
    <div>
      <h2>Live FATAL Event Feed</h2>
      <p>Total received: {logs.length}</p>

      <ResponsiveContainer width="100%"></ResponsiveContainer>
    </div>
  );
}
