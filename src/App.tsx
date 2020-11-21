import React from "react";
import "./App.css";
import logo from "./img/logo_in_app.png";

function App() {
  return (
    <div className="App">
      <div
        style={{
          textAlign: "center",
          backgroundColor: "#282A36",
          padding: "100px",
        }}
      >
        <img
          src={logo}
          aria-label="logo"
          alt="logo"
          style={{
            alignContent: "center",
            height: "50px",
            paddingTop: "10px",
          }}
        />
        <h3 style={{ color: "white" }}>XiT : eXcel Interaction Tool</h3>
        <h4 style={{ color: "white" }}>
          <a
            href="https://github.com/howzitcal/xitool.ml_serve/releases/download/latest/xit-64bit-0.1.3.exe"
            style={{ color: "#FFD96A" }}
          >
            Download Latest
          </a>
        </h4>
        <p style={{ color: "grey" }}>
          <i>Developed by C.D. Fleming 2020</i>
        </p>
      </div>
    </div>
  );
}

export default App;
