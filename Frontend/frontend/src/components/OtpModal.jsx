import React, { useEffect, useRef, useState } from "react";

export default function OtpModal({ isOpen, email, currentOtp, onVerify, onClose, onResend }) {
  const [digits, setDigits] = useState(["", "", "", "", "", ""]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);
  const [resendMessage, setResendMessage] = useState("");
  const inputsRef = useRef([]);

  useEffect(() => {
    if (isOpen && inputsRef.current[0]) inputsRef.current[0].focus();
  }, [isOpen]);

  if (!isOpen) return null;

  const value = digits.join("");

  const handleChange = (index, val) => {
    const clean = val.replace(/\D/g, "").slice(0, 1);
    const next = [...digits];
    next[index] = clean;
    setDigits(next);
    if (clean && inputsRef.current[index + 1]) {
      inputsRef.current[index + 1].focus();
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === "Backspace" && !digits[index] && inputsRef.current[index - 1]) {
      inputsRef.current[index - 1].focus();
    }
  };

  const handlePaste = (e) => {
    const text = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6);
    if (!text) return;
    const arr = text.split("");
    const next = ["", "", "", "", "", ""];
    for (let i = 0; i < arr.length; i++) next[i] = arr[i];
    setDigits(next);
    const lastIndex = Math.min(arr.length, 6) - 1;
    if (inputsRef.current[lastIndex]) inputsRef.current[lastIndex].focus();
  };

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    const res = await onVerify(value);
    setLoading(false);
    if (res?.error) setError(res.error);
  };

  const handleResend = async () => {
    if (resendLoading) return; // Prevent multiple simultaneous calls
    
    setResendLoading(true);
    setError("");
    setResendMessage("");
    
    try {
      const result = onResend && await onResend();
      if (result?.success) {
        setResendMessage("New code sent! Check your alert for the code.");
        setDigits(["", "", "", "", "", ""]);
        if (inputsRef.current[0]) inputsRef.current[0].focus();
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
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex",
      alignItems: "center", justifyContent: "center", padding: 16, zIndex: 1000
    }}>
      <div className="card" style={{ maxWidth: 420 }}>
        <h3>2‑Step Verification</h3>
        <p>Enter the 6‑digit code sent to {email}</p>
        {/* Code is alerted; not shown inline */}
        <form onSubmit={submit}>
          <div style={{ display: "flex", gap: 8, justifyContent: "center", marginBottom: 12 }} onPaste={handlePaste}>
            {digits.map((d, i) => (
              <input
                key={i}
                ref={(el) => (inputsRef.current[i] = el)}
                value={d}
                onChange={(e) => handleChange(i, e.target.value)}
                onKeyDown={(e) => handleKeyDown(i, e)}
                inputMode="numeric"
                pattern="[0-9]{1}"
                style={{ width: 42, textAlign: "center" }}
              />
            ))}
          </div>
          <div className="actions" style={{ justifyContent: "center" }}>
            <button type="submit" disabled={loading || value.length !== 6}>
              {loading ? "Verifying..." : "Verify"}
            </button>
          </div>
          {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
          {resendMessage && <p style={{ color: "green", textAlign: "center" }}>{resendMessage}</p>}
        </form>
        <div className="actions" style={{ justifyContent: "space-between", marginTop: 12 }}>
          <button onClick={onClose}>Cancel</button>
          {onResend && (
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
          )}
        </div>
      </div>
    </div>
  );
}


