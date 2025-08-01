import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './components/LandingPage';
import HomePage from './components/HomePage';
import DefaulterPrediction from './components/DefaulterPrediction';
import LastKnownLocation from './components/LastKnownLocation';
import LoanApproval from './components/LoanApproval';

function App() {
  return (
    <Router>
      <Routes>
        {/* Landing page without navbar/footer */}
        <Route path="/" element={<LandingPage />} />
        
        {/* Dashboard pages with navbar/footer */}
        <Route path="/home" element={
          <div className="min-h-screen bg-gray-50 flex flex-col">
            <Navbar />
            <div className="flex-1 pt-16">
              <HomePage />
            </div>
            <Footer />
          </div>
        } />
        <Route path="/defaulter-prediction" element={
          <div className="min-h-screen bg-gray-50 flex flex-col">
            <Navbar />
            <div className="flex-1 pt-16">
              <DefaulterPrediction />
            </div>
            <Footer />
          </div>
        } />
        <Route path="/last-known-location" element={
          <div className="min-h-screen bg-gray-50 flex flex-col">
            <Navbar />
            <div className="flex-1 pt-16">
              <LastKnownLocation />
            </div>
            <Footer />
          </div>
        } />
        <Route path="/loan-approval" element={
          <div className="min-h-screen bg-gray-50 flex flex-col">
            <Navbar />
            <div className="flex-1 pt-16">
              <LoanApproval />
            </div>
            <Footer />
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;