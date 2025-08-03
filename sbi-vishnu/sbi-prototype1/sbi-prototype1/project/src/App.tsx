import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './components/LandingPage';
import HomePage from './components/HomePage';
import DefaulterPrediction from './components/DefaulterPrediction';
import LastKnownLocation from './components/LastKnownLocation';
import LoanApproval from './components/LoanApproval';
import ProtectedRoute from './components/ProtectedRoute'; // 🔐 Import

function App() {
  return (
    <Router>
      <Routes>
        {/* Public landing page (no auth) */}
        <Route path="/" element={<LandingPage />} />

        {/* Protected Dashboard routes */}
        <Route path="/home" element={
          <ProtectedRoute>
            <div className="min-h-screen bg-gray-50 flex flex-col">
              <Navbar />
              <div className="flex-1 pt-16">
                <HomePage />
              </div>
              <Footer />
            </div>
          </ProtectedRoute>
        } />

        <Route path="/defaulter-prediction" element={
          <ProtectedRoute>
            <div className="min-h-screen bg-gray-50 flex flex-col">
              <Navbar />
              <div className="flex-1 pt-16">
                <DefaulterPrediction />
              </div>
              <Footer />
            </div>
          </ProtectedRoute>
        } />

        <Route path="/last-known-location" element={
          <ProtectedRoute>
            <div className="min-h-screen bg-gray-50 flex flex-col">
              <Navbar />
              <div className="flex-1 pt-16">
                <LastKnownLocation />
              </div>
              <Footer />
            </div>
          </ProtectedRoute>
        } />

        <Route path="/loan-approval" element={
          <ProtectedRoute>
            <div className="min-h-screen bg-gray-50 flex flex-col">
              <Navbar />
              <div className="flex-1 pt-16">
                <LoanApproval />
              </div>
              <Footer />
            </div>
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;
