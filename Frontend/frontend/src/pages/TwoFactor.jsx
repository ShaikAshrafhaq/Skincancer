import React, { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { useAuth } from "../state/AuthContext.jsx";

export default function TwoFactor() {
  const navigate = useNavigate();
  const { pendingUser, verifyOtp, requestNewOtp } = useAuth();
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);
  const [resendMessage, setResendMessage] = useState("");

  if (!pendingUser) {
    return <Navigate to="/login" replace />;
  }

  const onVerify = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    const res = await verifyOtp(otp);
    setLoading(false);
    if (res?.error) {
      setError(res.error);
    } else {
      navigate("/dashboard", { replace: true });
    }
  };

  const handleResend = async () => {
    if (resendLoading) return; // Prevent multiple simultaneous calls
    
    setResendLoading(true);
    setError("");
    setResendMessage("");
    
    try {
      const result = await requestNewOtp();
      if (result?.success) {
        setResendMessage("New code sent! Check your alert for the code.");
        setOtp("");
      } else if (result?.error) {
        setError(result.error);
      }
    } catch (err) {
      setError("Failed to resend code. Please try again.");
    } finally {
      setResendLoading(false);
    }
  };

  return (
    <div className="card" style={{ margin: "0 auto" }}>
      <h2>Two-Factor Authentication</h2>
      <p>We sent a 6-digit code to {pendingUser.email}</p>
      <form onSubmit={onVerify}>
        <div style={{ display: "flex", gap: 8 }}>
          <input
            type="text"
            inputMode="numeric"
            pattern="[0-9]{6}"
            placeholder="Enter 6-digit code"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? "Verifying..." : "Verify"}
          </button>
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        {resendMessage && <p style={{ color: "green" }}>{resendMessage}</p>}
      </form>
      <div style={{ marginTop: 16, textAlign: "center" }}>
        <button 
          onClick={handleResend} 
          disabled={resendLoading}
          style={{ 
            opacity: resendLoading ? 0.6 : 1,
            cursor: resendLoading ? 'not-allowed' : 'pointer'
          }}
        >
          {resendLoading ? "Sending..." : "Resend code"}
        </button>
      </div>
    </div>
  );
}


