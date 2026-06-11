import { useState, useEffect } from 'react'
import BatchResults from './components/BatchResults'
import LiveFeed from './components/LiveFeed'
import AlertPanel from './components/AlertPanel'

function App() {
  // State to hold batch results
  const [batchResults, setBatchResults] = useState(null)
  // State to hold live feed logs
  const [fatalLogs, setFatalLogs] = useState([])
  // Effect to fetch batch results on component mount 
  useEffect(() => {
    // Fetch batch results from the backend API
    fetch('http://localhost:8000/results')
      .then(response => response.json())
      .then(data => setBatchResults(data))
      .catch(error => console.error('Error fetching batch results:', error))
  }, [])

  // Effect to connect to WebSocket for live feed on component mount
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/stream')

    ws.onmessage = (event) => {

      setFatalLogs(prevLogs => [...prevLogs, event.data])

    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    // Clean up WebSocket connection on component unmount
    return () => {
      ws.close()
    }
  }, [])

  return (
    <div>
      <h1>Log Analysis Dashboard</h1>
      <BatchResults data={batchResults} />
      <LiveFeed logs={fatalLogs} />
      <AlertPanel logs={fatalLogs} />
    </div>
  )

}

export default App