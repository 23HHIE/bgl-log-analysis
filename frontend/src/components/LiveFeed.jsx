import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function LiveFeed({ logs }) {
  // 每10条日志作为一个数据点，显示累计 FATAL 事件数量趋势
  const chartData = logs
    .filter((_, i) => i % 10 === 0)
    .map((_, i) => ({
      index: i * 10,
      total: i * 10
    }))

  return (
    <div>
      <h2>Live FATAL Event Feed</h2>
      <p>Total received: {logs.length}</p>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="index" label={{ value: 'Events processed', position: 'bottom' }} />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="total" stroke="#ff4444" dot={false} />
        </LineChart>
      </ResponsiveContainer>

      <h3>Recent Logs</h3>
      <div style={{ height: '200px', overflowY: 'scroll', fontFamily: 'monospace', fontSize: '11px' }}>
        {logs.slice(-50).reverse().map((log, i) => (
          <div key={i}>{log}</div>
        ))}
      </div>
    </div>
  )
}

export default LiveFeed
