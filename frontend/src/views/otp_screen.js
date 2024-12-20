import React from 'react'
import Otp from './otp'
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

const Otp_screen = () => {
  const navigate=useNavigate()
  
  useEffect(() => {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      const value = localStorage.getItem(key);
      console.log(`Key: ${key}, Value: ${value}`);
      
    }
  }, []);
  const handleOtpSubmit = async (otp) => {
    var email = localStorage.getItem("email")
    try {
      alert(`Submitted OTP: ${otp}`);
      console.log(email)
      // Make API call to validate OTP
      const response = await fetch("http://127.0.0.1:8000/api/validate-otp/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email,
          otp
        })
      });

      const data = await response.json();
      console.log(data);

      if (response.status === 200) {
        navigate("/commands");
      } else {
        alert(data.message || "Failed to validate OTP");
      }
    } catch (error) {
      console.error("Error during OTP validation:", error);
      alert("Something went wrong. Please try again.");
    }
  };
  return (
    <Otp length={6} onSubmit={handleOtpSubmit} />
  )
}

export default Otp_screen