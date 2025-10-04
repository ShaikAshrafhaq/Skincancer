import React, { createContext, useContext, useMemo, useState } from "react";
import apiService from "../services/api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [pendingUser, setPendingUser] = useState(null); // holds email during 2FA

  // User storage key for localStorage
  const USERS_STORAGE_KEY = 'skincancer_users';

  const generateSixDigitOtp = () => {
    const num = Math.floor(Math.random() * 1000000);
    return String(num).padStart(6, "0");
  };

  // Get all users from localStorage
  const getUsers = () => {
    try {
      const users = localStorage.getItem(USERS_STORAGE_KEY);
      return users ? JSON.parse(users) : [];
    } catch (error) {
      console.error('Error loading users:', error);
      return [];
    }
  };

  // Save users to localStorage
  const saveUsers = (users) => {
    try {
      localStorage.setItem(USERS_STORAGE_KEY, JSON.stringify(users));
    } catch (error) {
      console.error('Error saving users:', error);
    }
  };

  // Check if user exists
  const userExists = (email) => {
    const users = getUsers();
    return users.some(user => user.email === email);
  };

  // Get user by email
  const getUserByEmail = (email) => {
    const users = getUsers();
    return users.find(user => user.email === email);
  };

  const loginWithPassword = async (email, password) => {
    // Validate input
    if (!email || !password) {
      return { error: "Please enter both email and password" };
    }

    if (password.length < 6) {
      return { error: "Password must be at least 6 characters" };
    }

    try {
      // Try to login with backend API
      const response = await apiService.login(email, password);
      
      if (response.requires2FA) {
        // Generate OTP for 2FA
        const otp = generateSixDigitOtp();
        setPendingUser({ 
          email, 
          name: response.user?.name || email, 
          otp,
          isLogin: true 
        });
        try { window.alert(`Your OTP code is: ${otp}`); } catch (_) {}
        return { requires2FA: true };
      } else if (response.token) {
        // Direct login success
        localStorage.setItem('authToken', response.token);
        setIsAuthenticated(true);
        return { success: true, message: "Login successful!" };
      }
    } catch (error) {
      // Fallback to local storage check for demo
      if (!userExists(email)) {
        return { error: "Invalid user - Account does not exist" };
      }

      const user = getUserByEmail(email);
      if (!user) {
        return { error: "Invalid user - Account not found" };
      }

      // Generate OTP and proceed to 2FA
      const otp = generateSixDigitOtp();
      setPendingUser({ 
        email, 
        name: user.name, 
        otp,
        isLogin: true 
      });
      try { window.alert(`Your OTP code is: ${otp}`); } catch (_) {}
      return { requires2FA: true };
    }
  };

  const registerAccount = async (name, email, password) => {
    // Validate input
    if (!name || !email || !password) {
      return { error: "Please fill in all fields" };
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return { error: "Please enter a valid email address" };
    }

    // Validate password strength
    if (password.length < 6) {
      return { error: "Password must be at least 6 characters" };
    }

    try {
      // Try to register with backend API
      const response = await apiService.register({ name, email, password });
      
      if (response.requires2FA) {
        // Generate OTP for 2FA
        const otp = generateSixDigitOtp();
        setPendingUser({ 
          email, 
          name, 
          otp,
          isSignup: true 
        });
        try { window.alert(`Your OTP code is: ${otp}`); } catch (_) {}
        return { requires2FA: true };
      } else if (response.token) {
        // Direct registration success
        localStorage.setItem('authToken', response.token);
        setIsAuthenticated(true);
        return { success: true, message: "Account created successfully!" };
      }
    } catch (error) {
      // Fallback to local storage check for demo
      if (userExists(email)) {
        return { error: "Account already exists with this email" };
      }

      // Create new user object
      const newUser = {
        id: Date.now().toString(), // Simple ID generation
        name: name.trim(),
        email: email.toLowerCase().trim(),
        password: password, // In real app, this would be hashed
        createdAt: new Date().toISOString(),
        isVerified: false
      };

      // Generate OTP for verification
      const otp = generateSixDigitOtp();
      setPendingUser({ 
        email: newUser.email, 
        name: newUser.name, 
        otp,
        newUser: newUser,
        isSignup: true 
      });
      try { window.alert(`Your OTP code is: ${otp}`); } catch (_) {}
      return { requires2FA: true };
    }
  };

  const verifyOtp = async (otp) => {
    // Validate OTP format
    if (!pendingUser || !/^\d{6}$/.test(otp)) {
      return { error: "Invalid code format" };
    }

    // Verify OTP matches
    if (pendingUser.otp !== otp) {
      return { error: "Invalid code - Please try again" };
    }

    // Handle signup flow
    if (pendingUser.isSignup && pendingUser.newUser) {
      // Save new user to localStorage
      const users = getUsers();
      users.push(pendingUser.newUser);
      saveUsers(users);
      
      setIsAuthenticated(true);
      setPendingUser(null);
      return { success: true, message: "Account created successfully!" };
    }

    // Handle login flow
    if (pendingUser.isLogin) {
      setIsAuthenticated(true);
      setPendingUser(null);
      return { success: true, message: "Login successful!" };
    }

    // Fallback for other cases
    setIsAuthenticated(true);
    setPendingUser(null);
    return { success: true };
  };

  const requestNewOtp = () => {
    if (!pendingUser) return { error: "No pending user" };
    const otp = generateSixDigitOtp();
    setPendingUser({ ...pendingUser, otp });
    try { window.alert(`Your new OTP code is: ${otp}`); } catch (_) {}
    return { success: true };
  };

  const logout = () => {
    setIsAuthenticated(false);
    setPendingUser(null);
  };

  // Get current user info
  const getCurrentUser = () => {
    if (!isAuthenticated || !pendingUser) return null;
    return {
      email: pendingUser.email,
      name: pendingUser.name
    };
  };

  const value = useMemo(
    () => ({ 
      isAuthenticated, 
      pendingUser, 
      loginWithPassword, 
      registerAccount, 
      verifyOtp, 
      requestNewOtp, 
      logout,
      getCurrentUser,
      userExists,
      getUserByEmail
    }),
    [isAuthenticated, pendingUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}


