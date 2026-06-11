function AlertPanel({ logs }) {
  return (
    <div>
      <h2>FATAL Alert Panel</h2>
      <p>Total FATAL events received: {logs.length}</p>
      <h3>Latest 5 Alerts</h3>
      <ul>
        {logs.slice(-5).reverse().map((log, i) => (
          <li key={i} style={{ color: 'red', fontFamily: 'monospace', fontSize: '12px' }}>
            {log}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default AlertPanel
