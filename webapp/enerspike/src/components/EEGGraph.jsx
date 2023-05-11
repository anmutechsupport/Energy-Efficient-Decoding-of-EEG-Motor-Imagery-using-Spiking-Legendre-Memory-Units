import { useEffect, useState } from "react";

function EEGGraph() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const eventSource = new EventSource("http://127.0.0.1:5000/stream");

    eventSource.onmessage = (event) => {
      const newData = JSON.parse(event.data);
      console.log(newData);
      setData(newData);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  // Render the graph using the data state
}

export default EEGGraph;
