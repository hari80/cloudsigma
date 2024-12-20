import React from 'react'

import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import PrivateRoute from "./utils/PrivateRoute"
import { AuthProvider } from './context/AuthContext'

import Homepage from './views/Homepage'
import Registerpage from './views/Registerpage'
import Loginpage from './views/Loginpage'
import Dashboard from './views/Dashboard'
import Otp_screen from './views/otp_screen'
import Navbar from './views/Navbar'
import MyForm from './views/commands'



function App() {
  return (
    <Router>
      <AuthProvider>
        < Navbar/>
        <Routes>
          
          <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/otpscreen"
          element={
            <PrivateRoute>
              <Otp_screen></Otp_screen>
            </PrivateRoute>
          }
        />
        <Route
          path="/commands"
          element={
            <PrivateRoute>
              <MyForm></MyForm>
            </PrivateRoute>
          }
        />
          <Route  path="/login" element={<Loginpage />} />
          <Route  path="/register" element={<Registerpage />} />
          <Route  path="/" element={<Homepage />} />
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App