import React, { } from 'react';
import './App.css';

import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

import LandingPage from "./pages/Landing";
import LoginPage from './pages/Login'
import RegisterPage from './pages/Register'
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <div className="vh-100 gradient-custom">
      <div className="container">
        <h1 className="page-header text-center">React and Python Flask Login Register</h1>

        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;