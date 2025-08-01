import React from 'react';
import { Link } from 'react-router-dom';
import { TrendingDown, MapPin, BadgeCheck } from 'lucide-react';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="text-center mb-12 pt-8">
          <h1 className="text-4xl md:text-5xl font-bold text-sbi-blue mb-4">
            Welcome to SBI Analytics Hub
          </h1>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Advanced analytics and prediction tools for enhanced banking operations
          </p>
        </div>

        {/* Main Options */}
        <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8">
          {/* Defaulter Prediction Card */}
          <Link to="/defaulter-prediction" className="group">
            <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 border border-gray-100 hover:border-sbi-blue/20 transform hover:-translate-y-1">
              <div className="flex items-center justify-center w-16 h-16 bg-sbi-blue/10 rounded-full mb-6 group-hover:bg-sbi-blue/20 transition-colors">
                <TrendingDown className="w-8 h-8 text-sbi-blue" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Defaulter Prediction
              </h2>
              <p className="text-gray-600 mb-6 leading-relaxed">
                Analyze customer profiles and predict loan default probability using advanced machine learning algorithms.
              </p>
              <div className="flex items-center text-sbi-blue font-semibold group-hover:text-blue-700">
                Get Started
                <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </Link>

          {/* Last Known Location Card */}
          <Link to="/last-known-location" className="group">
            <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 border border-gray-100 hover:border-sbi-blue/20 transform hover:-translate-y-1">
              <div className="flex items-center justify-center w-16 h-16 bg-sbi-blue/10 rounded-full mb-6 group-hover:bg-sbi-blue/20 transition-colors">
                <MapPin className="w-8 h-8 text-sbi-blue" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Last Known Location
              </h2>
              <p className="text-gray-600 mb-6 leading-relaxed">
                Track customer location using tower logs data for enhanced security and customer service operations.
              </p>
              <div className="flex items-center text-sbi-blue font-semibold group-hover:text-blue-700">
                Get Started
                <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </Link>

          {/* Loan Approval Prediction Card */}
          <Link to="/loan-approval" className="group">
            <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 border border-gray-100 hover:border-sbi-blue/20 transform hover:-translate-y-1">
              <div className="flex items-center justify-center w-16 h-16 bg-sbi-blue/10 rounded-full mb-6 group-hover:bg-sbi-blue/20 transition-colors">
                <BadgeCheck className="w-8 h-8 text-sbi-blue" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Loan Approval Prediction
              </h2>
              <p className="text-gray-600 mb-6 leading-relaxed">
                Assess user profiles and generate instant loan approval predictions to streamline decision-making.
              </p>
              <div className="flex items-center text-sbi-blue font-semibold group-hover:text-blue-700">
                Get Started
                <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
