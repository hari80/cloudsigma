import React, { useState } from "react";
import { useEffect } from "react";
import "../myform.css";

const frmCss = {
  width: "300px",
  margin: "200px auto",
  padding: "20px",
  border: "1px solid #ccc",
  borderRadius: "8px",
  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  fontSize: "1em",
  fontFamily: "Arial, sans-serif",
  backgroundColor: "#f9f9f9",
};

const inputCss = {
  width: "100%",
  padding: "10px",
  margin: "10px 0",
  boxSizing: "border-box",
  border: "1px solid #ccc",
  borderRadius: "4px",
};

const buttonCss = {
  width: "100%",
  padding: "10px",
  backgroundColor: "#007bff",
  color: "#fff",
  border: "none",
  borderRadius: "4px",
  cursor: "pointer",
  fontSize: "1em",
};

const logCss = {
  marginTop: "20px",
  padding: "10px",
  border: "1px solid #ccc",
  borderRadius: "4px",
  backgroundColor: "#f1f1f1",
  maxHeight: "200px",
  overflowY: "auto",
};

const MyForm = () => {
    const [logs, setLogs] = useState([]);
    useEffect(() => {
        // Connect to the Django Channels WebSocket
        const logSocket = new WebSocket('ws://127.0.0.1:8000/ws/logs/');
    
        logSocket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          const logMessage = data.message;
          console.log(logMessage)
          // Append new log message to the logs state
          setLogs((prevLogs) => [...prevLogs, logMessage]);
        };
    
        logSocket.onclose = (event) => {
          console.log('WebSocket closed:', event);
        };
    
        return () => {
          logSocket.close();
        };
      }, []);
  // State for each input field
  const [formData, setFormData] = useState({
    field1: "",
    field2: "",
    field3: "",
    field4: "",
    field5: "",
  });

  // Handle change in input fields
  const handleChange = (e) => {
    const { name, value } = e.target;
    

  
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLogs([""]);
    console.log("Form Submitted", formData);
    if(formData.radioGroup == "sync")
    {
        var url="http://127.0.0.1:8000/api/commands/"
    }
    if(formData.radioGroup == "async")
    {
        var url="http://127.0.0.1:8000/api/commandsasync/"
    }
    try {
        
        // Make API call to validate OTP
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            formData
          })
        });
  
        const data = await response.json();
        console.log(data);
  
        if (response.status === 200) {
            const logSocket = new WebSocket('ws://127.0.0.1:8000/ws/logs/');
    
            logSocket.onmessage = (event) => {
              const data = JSON.parse(event.data);
              const logMessage = data.message;
              console.log(logMessage)
              // Append new log message to the logs state
              setLogs((prevLogs) => [...prevLogs, logMessage]);
            };
        
            logSocket.onclose = (event) => {
              console.log('WebSocket closed:', event);
            };
        
            return () => {
              logSocket.close();
            };
        } else {
          alert(data.message || "Error");
        }
      } catch (error) {
        console.error("Error during OTP validation:", error);
        alert("Something went wrong. Please try again.");
      }
    // You can send the form data to a backend here
  };

  return (
    <div>
        <div>
    <form onSubmit={handleSubmit} style={frmCss}>
      <div>
        <label htmlFor="field1">Field 1:</label>
        <input
          type="text"
          id="field1"
          name="field1"
          value={formData.field1}
          onChange={handleChange}
          style={inputCss}
        />
      </div>
      <div>
        <label htmlFor="field2">Field 2:</label>
        <input
          type="text"
          id="field2"
          name="field2"
          value={formData.field2}
          onChange={handleChange}
          style={inputCss}
        />
      </div>
      <div>
        <label htmlFor="field3">Field 3:</label>
        <input
          type="text"
          id="field3"
          name="field3"
          value={formData.field3}
          onChange={handleChange}
          style={inputCss}
        />
      </div>
      <div>
        <label htmlFor="field4">Field 4:</label>
        <input
          type="text"
          id="field4"
          name="field4"
          value={formData.field4}
          onChange={handleChange}
          style={inputCss}
        />
      </div>
      <div>
        <label htmlFor="field5">Field 5:</label>
        <input
          type="text"
          id="field5"
          name="field5"
          value={formData.field5}
          onChange={handleChange}
          style={inputCss}
        />
      </div>
      <div>
        <p>Choose an option:</p>
        <label>
          <input
            type="radio"
            name="radioGroup"
            value="sync"
            checked={formData.radioGroup === "sync"}
            onChange={handleChange}
            style={inputCss}
          />
          Synchronous
        </label>
        <label>
          <input
            type="radio"
            name="radioGroup"
            value="async"
            checked={formData.radioGroup === "async"}
            onChange={handleChange}
            style={inputCss}
          />
          Asynchronous
        </label>
        
      </div>
      <button type="submit" style={buttonCss}>Submit</button>
    </form>
    </div>
    <div>
      <h2>Real-Time Logs</h2>
      <ul>
        {logs.map((log, index) => (
          <li key={index}>{log}<br></br><br></br></li>
          
        ))}
      </ul>
    </div>
    </div>
  );
};

export default MyForm;
