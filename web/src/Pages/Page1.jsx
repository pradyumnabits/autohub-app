import React, { useState, useEffect } from "react";
import HomeLayout from "../Layouts/HomeLayout";
import axios from "axios";
import { Link } from "react-router-dom";

function Page1() {
  return (
    <HomeLayout>
      <Dashboard />
    </HomeLayout>
  );
}

function Dashboard() {
  const [expandedSection, setExpandedSection] = useState(null);
  const [loading, setLoading] = useState({
    user: true,
    bookedVehicles: true,
    testDriveVehicles: true,
    serviceHistory: true,
    roadSideAssistance: true,
    feedbackHistory: true ,
  });
  const [user, setUser] = useState(null);
  const [bookedVehicles, setBookedVehicles] = useState([]);
  const [testDriveVehicles, setTestDriveVehicles] = useState([]);
  const [serviceHistory, setServiceHistory] = useState([]);
  const [roadSideAssistance, setRoadSideAssistance] = useState([]);
  const [feedbackHistory, setFeedbackHistory] = useState([]);

  useEffect(() => {
    const user = localStorage.getItem("user");
    const userId = JSON.parse(user);
    axios
      .get(`http://localhost:8007/customers/${userId.userName}`)
      .then((response) => {
        setUser(response.data);
        setLoading((prev) => ({ ...prev, user: false }));
      })
      .catch(() => setLoading((prev) => ({ ...prev, user: false })));

    // Fetch Vehicles
    axios
      .get(`http://localhost:8003/bookings?user_name=${userId.userName}`)
      .then((response) => {
        setBookedVehicles(response.data);
        setLoading((prev) => ({ ...prev, vehicles: false }));
      })
      .catch(() => setLoading((prev) => ({ ...prev, vehicles: false })));

    // fetch TestDrive vehiclies
    axios
      .get(`http://localhost:8003/testdrives?user_name=${userId.userName}`)
      .then((response) => {
        setTestDriveVehicles(response.data);
        setLoading((prev) => ({ ...prev, testDrives: false }));
      })
      .catch(() => setLoading((prev) => ({ ...prev, testDrives: false })));
      const fetchServiceHistory = async () => {
        try {
          const response = await axios.get(
            `http://localhost:8004/service/history?user_id=${userId.userName}`
          );
          setServiceHistory(response.data);
        } catch (error) {
          console.error("Error fetching service history:", error);
        } finally {
          setLoading((prev) => ({ ...prev, serviceHistory: false }));
        }
      };
      fetchServiceHistory();
      // fetch Road Side Assistance
      const fetchRsaHistory = async () => {
        try {
          const response = await axios.get(
            `http://localhost:8005/rsa/requests?userId=${userId.userName}`
          );
          setRoadSideAssistance(response.data);
        } catch (error) {
          console.error("Error fetching service history:", error);
        } finally {
          setLoading((prev) => ({ ...prev, roadSideAssistance: false }));
        }
      };
      fetchRsaHistory();
      // Fetch feedback history
    const fetchFeedbackHistory = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8006/feedback/history/${userId.userName}`
        );
        setFeedbackHistory(response.data);
      } catch (error) {
        console.error("Error fetching feedback history:", error);
      } finally {
        setLoading(prev => ({ ...prev, feedbackHistory: false }));
      }
    };
    fetchFeedbackHistory();
  }, []);

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  return (
    <div className="bg-gray-700 min-h-screen p-8 text-white">
      <div className="flex justify-end space-x-4 mb-6">
        <Link 
          to="/page2" 
          className="flex items-center bg-gray-800 hover:bg-gray-600 px-4 py-2 rounded-md"
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
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
            />
          </svg>
          Vehicles
        </Link>

        <Link 
          to="/page5" 
          className="flex items-center bg-gray-800 hover:bg-gray-600 px-4 py-2 rounded-md"
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
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          Road Side Assistance
        </Link>

        <Link 
          to="/page4" 
          className="flex items-center bg-gray-800 hover:bg-gray-600 px-4 py-2 rounded-md"
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
              d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          Support
        </Link>

        <Link 
          to="/page7" 
          className="flex items-center bg-gray-800 hover:bg-gray-600 px-4 py-2 rounded-md"
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
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          Feedback
        </Link>
      </div>

      <section className="bg-gray-800 p-6 rounded-md shadow-md mb-6 flex flex-row space-x-4">
        {loading.user ? (
          <Shimmer />
        ) : user ? (
          <div className="flex flex-row justify-between w-full">
            <div className="flex flex-col space-y-4">
              <h3 className="text-xl font-semibold">
                {user.firstName + " " + user.lastName}
              </h3>
              <div className="flex items-center space-x-2">
                <span className="text-gray-400">Email:</span>
                <a
                  href={`mailto:${user.email}`}
                  className="font-semibold hover:underline"
                >
                  {user.email}
                </a>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-gray-400">Phone Number:</span>
                <span className="font-semibold">{user.phoneNumber}</span>
              </div>
            </div>
            <div className="flex flex-col space-y-4">
              <div className="flex items-center space-x-2">
                <span className="text-gray-400">Address:</span>
                <span className="font-semibold">{user.address}</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-gray-400">Profile Status:</span>
                <span className="font-semibold text-green-500">
                  {user.profileStatus}
                </span>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-gray-400">User data could not be loaded.</p>
        )}
      </section>
      <div className="space-y-4">
        {/* Vehicles Section */}
        <CollapsibleSection
          title="Owned Vehicles"
          isOpen={expandedSection === "vehicles"}
          onToggle={() => toggleSection("vehicles")}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {bookedVehicles.map((vehicle) => (
              <VehicleCard key={vehicle.id} bookVehicle={vehicle} />
            ))}
          </div>
        </CollapsibleSection>
        {/* Test Drives Section */}
        <CollapsibleSection
          title="Test Drives"
          isOpen={expandedSection === "testDrives"}
          onToggle={() => toggleSection("testDrives")}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {testDriveVehicles.map((vehicle) => (
              <TestDriveCard key={vehicle.id} testDrive={vehicle} />
            ))}
          </div>
        </CollapsibleSection>
        {/* Service History Section */}
        <CollapsibleSection
          title="Service History"
          isOpen={expandedSection === "serviceHistory"}
          onToggle={() => toggleSection("serviceHistory")}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {serviceHistory.map((service, index) => (
              <ServiceCard 
                key={`${service.vehicle_id}-${service.service_date}-${index}`} 
                service={service} 
              />
            ))}
          </div>
          </CollapsibleSection>
          {/* Road Side Assistance Section */}
          <CollapsibleSection
          title="Road Side Assistance"
          isOpen={expandedSection === "RSA"}
          onToggle={() => toggleSection("RSA")}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {roadSideAssistance.map((rsa, index) => (
              <RSAHistoryCard 
                key={`${rsa.id}-${index}`} 
                rsa={rsa} 
              />
            ))}
          </div>
          </CollapsibleSection>
          {/* Feedback History Section */}
        <CollapsibleSection
          title="Feedback History"
          isOpen={expandedSection === "feedbackHistory"}
          onToggle={() => toggleSection("feedbackHistory")}
        >
          {loading.feedbackHistory ? (
            <div className="text-center text-gray-400">Loading feedback history...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {feedbackHistory.length > 0 ? (
                feedbackHistory.map((feedback) => (
                  <FeedbackCard key={feedback.feedback_id} feedback={feedback} />
                ))
              ) : (
                <p className="text-gray-400 col-span-full text-center">
                  No feedback history available.
                </p>
              )}
            </div>
          )}
        </CollapsibleSection>
      </div>
    </div>
  );
}

function Shimmer() {
  return (
    <div className="animate-pulse space-y-2">
      <div className="h-4 bg-gray-600 rounded w-1/2"></div>
      <div className="h-4 bg-gray-600 rounded w-3/4"></div>
      <div className="h-4 bg-gray-600 rounded w-1/3"></div>
    </div>
  );
}

function CollapsibleSection({ title, children, isOpen, onToggle }) {
  return (
    <section className="bg-gray-800 rounded-md shadow-md">
      <header
        onClick={onToggle}
        className="cursor-pointer p-4 flex justify-between items-center"
      >
        <h4 className="text-lg font-semibold">{title}</h4>
        <span>{isOpen ? "−" : "+"}</span>
      </header>
      {isOpen && <div className="p-4">{children}</div>}
    </section>
  );
}

function VehicleCard({ bookVehicle }) {
  const vehicle = bookVehicle.vehicle;
  return (
    <div className="bg-gray-900 p-4 rounded-md mb-2 shadow-md">
      <img
        src={vehicle.image_url}
        alt={`${vehicle.make} ${vehicle.model}`}
        className="w-full h-40 object-cover mb-4 rounded-md"
      />
      <h5 className="text-lg font-semibold">{`${vehicle.make} ${vehicle.model}`}</h5>
      <p>Price: ${vehicle.price}</p>
      <p>Year: {vehicle.year}</p>
      <p>Fuel Type: {vehicle.fuel_type}</p>
      <p>Transmission: {vehicle.transmission}</p>
      <p>Body Type: {vehicle.body_type}</p>
      <p>Transaction ID: {bookVehicle.transaction_id}</p>
      <p>Booking Date: {bookVehicle.booking_date}</p>
    </div>
  );
}

function TestDriveCard({ testDrive }) {
  const { vehicle, date, time, status } = testDrive;
  return (
    <div className="bg-gray-900 p-4 rounded-md mb-2 shadow-md">
      <img
        src={vehicle.image_url}
        alt={`${vehicle.make} ${vehicle.model}`}
        className="w-full h-40 object-cover mb-4 rounded-md"
      />
      <h5 className="text-lg font-semibold">{`${vehicle.make} ${vehicle.model}`}</h5>
      <p>Date: {date}</p>
      <p>Time: {time}</p>
      <p>Status: {status}</p>
    </div>
  );
}

function ServiceCard({ service }) {
  const { service_date, service_type, description, vehicle_details } = service;
  return (
    <div className="bg-gray-900 p-4 rounded-md mb-2 shadow-md">
      <img
        src={vehicle_details.image_url}
        alt={`${vehicle_details.make} ${vehicle_details.model}`}
        className="w-full h-40 object-cover mb-4 rounded-md"
      />
      <h5 className="text-lg font-semibold">
        {`${vehicle_details.year} ${vehicle_details.make} ${vehicle_details.model}`}
      </h5>
      <p>Service Date: {service_date}</p>
      <p>Service Type: {service_type}</p>
      <p>Status: {description}</p>
      <div className="mt-2 text-sm text-gray-400">
        <p>Vehicle Details:</p>
        <p>Fuel Type: {vehicle_details.fuel_type}</p>
        <p>Transmission: {vehicle_details.transmission}</p>
        <p>Body Type: {vehicle_details.body_type}</p>
      </div>
    </div>
  );
}

function RSAHistoryCard({ rsa }) {
  const { id, location, status, provider, vehicle_details } = rsa;
  return (
    <div className="bg-gray-900 p-4 rounded-md mb-2 shadow-md">
      <img
        src={vehicle_details.image_url}
        alt={`${vehicle_details.make} ${vehicle_details.model}`}
        className="w-full h-40 object-cover mb-4 rounded-md"
      />
      <h5 className="text-lg font-semibold">
        {`${vehicle_details.year} ${vehicle_details.make} ${vehicle_details.model}`}
      </h5>
      <div className="mt-4 space-y-2">
        <p>Request ID: {id.slice(0, 8)}...</p>
        <p>Location: {location}</p>
        <p>Status: <span className={`font-semibold ${status === 'Pending' ? 'text-yellow-500' : 'text-green-500'}`}>{status}</span></p>
        {provider && <p>Service Provider: {provider}</p>}
      </div>
      <div className="mt-4 text-sm text-gray-400">
        <p>Vehicle Details:</p>
        <p>Fuel Type: {vehicle_details.fuel_type}</p>
        <p>Transmission: {vehicle_details.transmission}</p>
        <p>Body Type: {vehicle_details.body_type}</p>
      </div>
    </div>
  );
}

function FeedbackCard({ feedback }) {
  const getFeedbackTypeColor = (type) => {
    switch (type) {
      case 'vehicle':
        return 'text-blue-400';
      case 'service':
        return 'text-green-400';
      case 'dealership':
        return 'text-purple-400';
      default:
        return 'text-gray-400';
    }
  };

  const getRatingStars = (rating) => {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
      <div className="flex justify-between items-start mb-3">
        <h3 className={`text-lg font-semibold ${getFeedbackTypeColor(feedback.feedback_type)}`}>
          {feedback.feedback_type.charAt(0).toUpperCase() + feedback.feedback_type.slice(1)} Feedback
        </h3>
        <span className="text-yellow-400" title={`${feedback.rating} out of 5 stars`}>
          {getRatingStars(feedback.rating)}
        </span>
      </div>
      
      <p className="text-gray-300 mb-2">
        <span className="text-gray-400">Reference ID:</span> {feedback.reference_id}
        </p>
      
      <p className="text-gray-300 mb-3">
        {feedback.details}
      </p>
      
      <p className="text-sm text-gray-400">
        Submitted: {new Date(feedback.submitted_at).toLocaleDateString()}
      </p>
    </div>
  );
}

export default Page1;
