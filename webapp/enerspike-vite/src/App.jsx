import { useState, useEffect, useRef } from "react";
import "./App.css";
import EEGGraph from "./components/EEGGraph";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [procJson, setJson] = useState(null);
  const [play, setPlay] = useState(false);

  // const [CSPData, setCSPData] = useState([]);
  const CSPData = [];
  // const [CSPWin, setCSPWin] = useState([]);
  let CSPWin = [];
  const formRef = useRef(null);

  useEffect(() => {
    console.log("gang gang");
    console.log(procJson);
    // let timeChange;

    // if (timeChange) clearInterval(timeChange);
    // setInterval(() => shiftWindow(), 1000);

    // const shiftWindow = () => {
    //   if (CSPData.length > 5) {
    //     CSPData.reverse().pop();
    //     CSPData.reverse();
    //     CSPWin = CSPData.slice(5);
    //   }
    // };
  }, [play]);

  const handleSubmit = (event) => {
    event.preventDefault();
    alert(`Selected file - ${formRef.current.files[0].name}`);
    setSelectedFile(formRef.current.files[0]);
  };

  const procData = async () => {
    // serialize selectedFile and send to flask server in POST request
    // receive processed data from flask server
    // setJson to processed data
    const formData = new FormData();
    formData.append("file", selectedFile);

    const response = await axios.post(
      "http://127.0.0.1:5000/process",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    console.log(response);
    setJson(response.data);
  };

  useEffect(() => {
    if (selectedFile) {
      procData();
    }
  }, [selectedFile]);

  // useEffect(() =>  {

  // }, [timeChange])

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          ref={formRef}
          defaultValue={selectedFile}
          // onChange={(e) => setSelectedFile(e.target.files[0])}
        />
        <br />
        <button type="submit">Submit</button>
      </form>

      <EEGGraph />
      {procJson ? (
        <div>
          <button
            onClick={() => {
              setPlay(!play);
            }}
          >
            {!play ? "Start" : "Stop"}
          </button>
        </div>
      ) : null}
    </div>
  );
}

export default App;
