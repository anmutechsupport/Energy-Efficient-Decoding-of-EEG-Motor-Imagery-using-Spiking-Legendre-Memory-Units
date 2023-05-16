import { useState, useEffect, useRef } from "react";
import "./App.css";
import EEGGraph from "./components/EEGGraph";
import PSDGraph from "./components/PSDGraph";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [procJson, setJson] = useState(null);
  const [play, setPlay] = useState(false);
  const [sampleIdx, setSampleIdx] = useState(0);
  const [spectroImg, setSpectroImg] = useState(null);
  const [PSDWin, setPSDWin] = useState(null);
  const [trueLabel, setTrueLabel] = useState(null);
  const [predLabel, setPredLabel] = useState(null);
  const [CSPWin, setCSPWin] = useState(null);
  const [accuracy, setAccuracy] = useState(0);
  const formRef = useRef(null);

  const getSpectro = async () => {
    // make a post request that asks for the spectrogram of the current sample
    // and set the spectrogram to the response
    // post a json
    const data = {
      sampleIdx: sampleIdx,
    };
    const response = await axios.post("http://127.0.0.1:5000/spectro", data);
    console.log(response);
    setSpectroImg(response.data);
    return "pass";
  };

  const calcAccuracy = (sampleIdx) => {
    // take all true labels and predicted labels from state vars up until sampleIdx and calculate accuracy
    // set accuracy to the calculated accuracy

    const trueLabels = procJson.true_labels.slice(0, sampleIdx + 1);
    const predLabels = procJson.pred_labels.slice(0, sampleIdx + 1);
    let correct = 0;
    for (let i = 0; i < trueLabels.length; i++) {
      if (trueLabels[i] == predLabels[i]) {
        correct++;
      }
    }
    // if trueLabels.length == 0, set accuracy to 0

    if (trueLabels.length == 0) {
      setAccuracy(0);
    } else setAccuracy(correct / trueLabels.length);
  };

  useEffect(() => {
    if (!procJson) return;
    console.log("playback");
    // console.log(procJson);

    let time = 0;
    let playbackInterval;

    if (play && sampleIdx < procJson.epochs_transformed.length) {
      playbackInterval = setInterval(() => {
        // Here you would define your logic to pull new data from procJson and append it to CSPWin
        // For example, assuming procJson is an array of data and you want to append one item per second:

        // const nextData = procJson.shift(); // remove the first item from procJson
        // setCSPWin((currentCSPWin) => [...currentCSPWin, nextData]); // append it to CSPWin
        if (time == 0) {
          getSpectro();
          setTrueLabel(procJson.true_labels[sampleIdx]);
          setPredLabel(procJson.pred_labels[sampleIdx]);
          calcAccuracy(sampleIdx);
        }
        if (time * 80 + 160 < procJson.epochs_transformed[0][0].length) {
          setCSPWin(
            procJson.epochs_transformed[sampleIdx].map((x) =>
              x.slice(time * 80, time * 80 + 160)
            )
          );
          const newPSDWin = [[], [], [], []];
          // get sampleIdx stft_data from procJson and loop through each channel and each frequency bin and pull the value from time index
          for (let ch = 0; ch < procJson.stft_data[sampleIdx].length; ch++) {
            for (
              let freq = 0;
              freq < procJson.stft_data[sampleIdx][0].length;
              freq++
            ) {
              newPSDWin[ch].push(procJson.stft_data[sampleIdx][ch][freq][time]);
            }
          }
          setPSDWin(newPSDWin);
          console.log(time);
          time++;
        } else {
          // time = 0;
          // getSpectro();
          setSampleIdx((sampleIdx) => sampleIdx + 1);
          // setCSPWin(
          //   procJson.epochs_transformed[sampleIdx].map((x) =>
          //     x.slice(time * 160, time * 160 + 160)
          //   )
          // );
          // console.log(time);
          // time++;
        }
      }, 500);
    } else {
      if (playbackInterval) clearInterval(playbackInterval);
      if (play) setPlay(false);
      if (sampleIdx >= procJson.epochs_transformed.length) {
        setSampleIdx(0);
      }
    }

    // Cleanup function
    return () => {
      if (playbackInterval) {
        clearInterval(playbackInterval);
      }
    };
  }, [play, procJson, sampleIdx]);

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
    return "pass";
  };

  useEffect(() => {
    if (selectedFile) {
      procData();
    }
  }, [selectedFile]);

  return (
    <div className="App">
      <h1> Enerspike Demo ⚡️ </h1>
      {procJson ? (
        <div>
          <h2>
            True Label: {trueLabel === 0 ? "hands" : trueLabel ? "feet" : null}
          </h2>
          <h2>
            Predicted Label:{" "}
            {predLabel === 0 ? "hands" : predLabel ? "feet" : null}
          </h2>
          <h2>Accuracy: {accuracy}</h2>
          <EEGGraph data={CSPWin} />
          <PSDGraph data={PSDWin} />
          {spectroImg ? (
            <div>
              <img src={`data:image/png;base64,${spectroImg}`} />
            </div>
          ) : null}
          <button
            onClick={() => {
              setPlay(!play);
            }}
          >
            {!play ? "Start" : "Stop"}
          </button>
        </div>
      ) : null}
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
    </div>
  );
}

export default App;
