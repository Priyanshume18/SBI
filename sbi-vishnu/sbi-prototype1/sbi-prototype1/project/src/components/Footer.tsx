import React from 'react';
import { Link } from 'react-router-dom';
import { Building2, Phone, Mail, MapPin, Shield, Award, Users, Globe } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-sbi-blue text-white">
      {/* Main Footer Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          {/* Company Info */}
          <div className="lg:col-span-1">
            <div className="flex items-center space-x-3 mb-4">
              <div className="flex items-center justify-center w-10 h-10 bg-white rounded-xl shadow-lg">
                <Building2 className="w-6 h-6 text-sbi-blue" />
              </div>
              <div>
                <h3 className="text-xl font-bold">SBI Analytics Hub</h3>
                <p className="text-sm text-blue-100">Advanced Banking Solutions</p>
              </div>
            </div>
            <p className="text-blue-100 text-sm leading-relaxed mb-4">
              Empowering banking operations with cutting-edge analytics and AI-driven insights for better decision making.
            </p>
            <div className="flex space-x-4">
              <div className="flex items-center space-x-2 text-blue-100">
                <Shield className="w-4 h-4" />
                <span className="text-xs">ISO 27001 Certified</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-blue-100 hover:text-white transition-colors text-sm">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/defaulter-prediction" className="text-blue-100 hover:text-white transition-colors text-sm">
                  Defaulter Prediction
                </Link>
              </li>
              <li>
                <Link to="/last-known-location" className="text-blue-100 hover:text-white transition-colors text-sm">
                  Location Tracking
                </Link>
              </li>
              <li>
                <Link to="/loan-approval" className="text-blue-100 hover:text-white transition-colors text-sm">
                  Loan Approval
                </Link>
              </li>
            </ul>
          </div>

          {/* Banking Services */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Banking Services</h4>
            <ul className="space-y-2">
              <li className="text-blue-100 hover:text-white transition-colors text-sm cursor-pointer">
                Personal Banking
              </li>
              <li className="text-blue-100 hover:text-white transition-colors text-sm cursor-pointer">
                Corporate Banking
              </li>
              <li className="text-blue-100 hover:text-white transition-colors text-sm cursor-pointer">
                Digital Banking
              </li>
              <li className="text-blue-100 hover:text-white transition-colors text-sm cursor-pointer">
                Investment Services
              </li>
              <li className="text-blue-100 hover:text-white transition-colors text-sm cursor-pointer">
                Insurance Products
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contact Information</h4>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Phone className="w-4 h-4 text-blue-200" />
                <span className="text-blue-100 text-sm">1800 425 3800</span>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-4 h-4 text-blue-200" />
                <span className="text-blue-100 text-sm">support@sbi.co.in</span>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="w-4 h-4 text-blue-200" />
                <span className="text-blue-100 text-sm">Mumbai, Maharashtra</span>
              </div>
              <div className="flex items-center space-x-3">
                <Globe className="w-4 h-4 text-blue-200" />
                <span className="text-blue-100 text-sm">www.sbi.co.in</span>
              </div>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-blue-600 mt-8 pt-8">
          <div className="flex flex-col lg:flex-row justify-between items-center space-y-4 lg:space-y-0">
            
            {/* Copyright */}
            <div className="text-blue-100 text-sm">
              <p>&copy; 2025 State Bank of India. All rights reserved.</p>
              <p className="mt-1">Built for SBI Hackathon 2025 • Advanced Analytics Prototype</p>
            </div>

            {/* Team Info */}
            <div className="text-right">
              <div className="text-blue-100 text-sm">
                <p className="font-semibold text-white mb-1">Team: <span className="text-blue-200">Idaten</span></p>
                <p className="text-xs text-blue-200">Creators:</p>
                <div className="text-xs text-blue-100 space-y-1">
                  <p>Priyanshu Maurya • Vishnu Singh</p>
                  <p>Anubhav Saha • Aditya Shahi</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-6 pt-6 border-t border-blue-600">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div className="flex items-center justify-center space-x-2">
              <Award className="w-4 h-4 text-blue-200" />
              <span className="text-blue-100 text-xs">Trusted by 45+ Crore Customers</span>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <Users className="w-4 h-4 text-blue-200" />
              <span className="text-blue-100 text-xs">22,000+ Branches Nationwide</span>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <Shield className="w-4 h-4 text-blue-200" />
              <span className="text-blue-100 text-xs">Banking Security Standards</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 