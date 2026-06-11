function BatchResults({ data }) {
  if (!data) return <p>Loading batch results...</p>

  return (
    <div>
      <h2>Batch Analysis Results</h2>

      <h3>Q10 — Top 3 Days of Week</h3>
      <ul>
        {data.q10_top_days.map((row, i) => (
          <li key={i}>Day {row.day_of_week}: {row.count.toLocaleString()} entries</li>
        ))}
      </ul>

      <h3>Q14 — Node with Most KERNRTSP Events</h3>
      <p>{data.q14_kernrtsp_node[0].node} — {data.q14_kernrtsp_node[0].count} events</p>

      <h3>Q7 — DDR Errors Weekly Average</h3>
      <p>Average per week: {data.q7_ddr_errors_weekly.average_per_week}</p>
    </div>
  )
}

export default BatchResults
