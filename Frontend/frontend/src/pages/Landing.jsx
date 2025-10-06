import React from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Landing() {
  const navigate = useNavigate();
  return (
    <div className="card">
      <h1>Welcome to Skin Cancer Detection</h1>
      <p>Analyze skin lesion images with confidence.</p>
      <button onClick={() => navigate("/get-started")}>
        Get Started
      </button>
      <div style={{ marginTop: 12 }}>
        <Link to="/signup">Create an account</Link>
      </div>
    </div>
  );
}


