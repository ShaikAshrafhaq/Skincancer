import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../state/AuthContext.jsx";
import OtpModal from "../components/OtpModal.jsx";

export default function Login() {
  const navigate = useNavigate();
  const { loginWithPassword, verifyOtp, pendingUser, requestNewOtp } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showOtp, setShowOtp] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    const res = await loginWithPassword(email, password);
    setLoading(false);
    if (res?.error) {
      setError(res.error);
    } else if (res?.requires2FA) {
      setShowOtp(true);
    }
  };

  return (
    <>
    <div className="card">
      <h2>Login</h2>
      <form onSubmit={onSubmit}>
        <div className="stack">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? "Checking..." : "Continue"}
          </button>
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </form>
      
      <p style={{ marginTop: 12 }}>
        New here? <Link to="/signup">Create an account</Link>
      </p>
    </div>
    {showOtp && (
      <OtpModal
        isOpen={showOtp}
        email={email}
        currentOtp={pendingUser?.otp}
        onVerify={async (code) => {
          const res = await verifyOtp(code);
          if (res?.success) {
            setShowOtp(false);
            // Show success message briefly before navigating
            if (res.message) {
              alert(res.message);
            }
            navigate("/dashboard", { replace: true });
          }
          return res;
        }}
        onResend={async () => {
          const result = await requestNewOtp();
          return result;
        }}
        onClose={() => setShowOtp(false)}
      />
    )}
    </>
  );
}


