function BatchResults(data) {
  if (!data) return <p>Loading batch results...</p>;

  return (
    <div>
      <h2>Batch Analysis Results</h2>
      <h3>Top 10 Most Frequent Fatal Errors</h3>
      <ul>
        {data.q10_top_days.map((row, i) => (
          <li key={i}>
            {row.day_of_week} - {row.count.toLocaleString()} entries
          </li>
        ))}
      </ul>

      <h3>Node with Most KERNRTSP Events</h3>
      <p>
        {data.q14_top_kernrtsp_node[0].node} -
        {data.q14_top_kernrtsp_node[0].count} events
      </p>

      <h3>DDR Errors Weekly Average</h3>
      <p>Average per week: {data.q7_ddr_errors_weekly.average_per_week}</p>
    </div>
  );
}

export default BatchResults;
