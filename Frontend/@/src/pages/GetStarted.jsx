import React from "react";
import { Link } from "react-router-dom";

export default function GetStarted() {
  return (
    <div className="card">
      <h2>Get Started</h2>
      <p>Choose how you want to continue.</p>
      <div className="actions" style={{ justifyContent: "center", marginTop: 12 }}>
        <Link to="/login"><button>Login</button></Link>
        <Link to="/signup"><button>Sign up</button></Link>
      </div>
    </div>
  );
}


