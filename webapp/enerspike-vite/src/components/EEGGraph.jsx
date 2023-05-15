import { useEffect, useState, useRef } from "react";
import {
  LineChart,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Line,
  Legend,
  ResponsiveContainer,
} from "recharts";

function EEGGraph({ data }) {
  const channelColors = useRef([]); // Ref to store the channel colors
  const [dataFilled, setDataFilled] = useState(false);
  const channels = useRef([]);
  const [formattedData, setFormattedData] = useState([{}]);

  useEffect(() => {
    // Generate colors for each channel once on mount
    if (data) setFormattedData(formatData(data));
    if (dataFilled) return;
    if (!data) return;
    channels.current = Array.from({ length: data.length }, (_, i) => i + 1);
    channelColors.current = Array.from({ length: data.length }, () => {
      const r = Math.floor(Math.random() * 256);
      const g = Math.floor(Math.random() * 256);
      const b = Math.floor(Math.random() * 256);
      return `rgb(${r}, ${g}, ${b})`;
    });
    setDataFilled(true);
  }, [data]);

  const formatXAxis = (tickItem) => {
    // 160 samples per second, so each tick represents 1/160th of a second
    return `${tickItem / 160}s`;
  };

  const formatData = (arr) => {
    let formattedData = [];

    for (let i = 0; i < arr[0].length; i++) {
      let dataPoint = { ts: i };
      for (let ch = 0; ch < arr.length; ch++) {
        dataPoint[`ch${ch + 1}`] = data[ch][i];
      }
      formattedData.push(dataPoint);
    }

    return formattedData;
  };

  if (data) {
    return (
      <LineChart
        width={1000} // Set the width to a fixed value
        height={600}
        data={formattedData}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="ts"
          tickFormatter={formatXAxis}
          type="number"
          domain={["dataMin", "dataMax"]}
        />
        <YAxis
          label={{
            value: "Microvolts (µV)",
            angle: -90,
            position: "insideLeft",
          }}
        />
        <Tooltip />
        <Legend />
        {channels.current.map((channel) => (
          <Line
            key={`ch${channel}`}
            type="monotone"
            dataKey={`ch${channel}`}
            stroke={channelColors.current[channel - 1]}
            activeDot={false}
            dot={false}
            // isAnimationActive={false}
          />
        ))}
      </LineChart>
    );
  } else {
    return null;
  }
}

export default EEGGraph;
