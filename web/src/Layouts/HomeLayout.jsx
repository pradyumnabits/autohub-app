// src/Layouts/HomeLayout.jsx
import React from "react";
import { Link, useLocation } from "react-router-dom";

function HomeLayout({ children }) {
  const location = useLocation();
  const isHomePage = location.pathname === '/';
  const showDashboard = ['/dashboard', '/catalog', '/testdrivebook', '/support', '/rsa', '/book', '/feedbackp'].includes(location.pathname);

  return (
    <div>
      <nav className="bg-gray-800 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <Link to="/" className="text-white text-xl font-bold">
            AutoHub
          </Link>
          
          <div className="space-x-4">
            {showDashboard && (
              <Link
                to="/dashboard"
                className="text-white hover:text-gray-300 transition flex items-center"
              >
                <svg 
                  className="w-5 h-5 mr-2" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth="2" 
                    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                  />
                </svg>
                Dashboard
              </Link>
            )}
            {isHomePage && (
              <>
                <Link
                  to="/login"
                  className="text-white hover:text-gray-300 transition"
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>
      {children}
    </div>
  );
}

export default HomeLayout;
