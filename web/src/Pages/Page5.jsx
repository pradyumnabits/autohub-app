import React, { useState, useEffect } from "react";
import HomeLayout from "../Layouts/HomeLayout";
import axios from "axios";
import Lottie from 'lottie-react';
import carAnimation from '../assets/Images/SSO_Icons/car-loading.json'; // Update path as needed
import Snackbar from '../components/Snackbar'; // Add this import at the top

// page for Roadside Assistance
function Page5() {
  return (
    <HomeLayout>
      <RoadsideAssistance />
    </HomeLayout>
  );
}

function RoadsideAssistance() {
  const [bookedVehicles, setBookedVehicles] = useState([]);
  const [rsaHistory, setRsaHistory] = useState([]);
  const [loadingVehicles, setLoadingVehicles] = useState(true);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [selectedVehicle, setSelectedVehicle] = useState(null);
  const [location, setLocation] = useState("");
  const [contactNumber, setContactNumber] = useState("");
  const [assistanceType, setAssistanceType] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  // Fetch booked vehicles
  useEffect(() => {
    const user = localStorage.getItem("user");
    const userId = JSON.parse(user);
    const fetchBookedVehicles = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8003/bookings?user_name=${userId.userName}`
        );
        setBookedVehicles(response.data);
      } catch (error) {
        console.error("Error fetching booked vehicles:", error);
      } finally {
        setLoadingVehicles(false);
      }
    };
    fetchBookedVehicles();
  }, []);

  // Fetch service history
  useEffect(() => {
    const user = localStorage.getItem("user");
    const userId = JSON.parse(user);
    const fetchRsaHistory = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8005/rsa/requests?userId=${userId.userName}`
        );
        setRsaHistory(response.data);
      } catch (error) {
        console.error("Error fetching service history:", error);
      } finally {
        setLoadingHistory(false);
      }
    };
    fetchRsaHistory();
  }, []);

  const handleOpenModal = (vehicle) => {
    setSelectedVehicle(vehicle);
  };

  const handleCloseModal = () => {
    setSelectedVehicle(null);
    setLocation("");
  };

  // Submit new service request
  const handleAppointmentSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    const user = localStorage.getItem("user");
    const userId = JSON.parse(user);
    try {
      const response = await axios.post("http://localhost:8005/rsa/requests", {
        vehicle_id: selectedVehicle.id,
        user_id: userId.userName,
        location,
        contact_number: contactNumber,
        assistance_type: assistanceType,
      });
      setRsaHistory([...rsaHistory, response.data]);
      handleCloseModal();
      
      // Show success message
      setSnackbarMessage('Roadside assistance request submitted successfully!');
      setShowSnackbar(true);
      setTimeout(() => setShowSnackbar(false), 3000);
      
    } catch (error) {
      console.error("Error submitting service request:", error);
      // Show error message
      setSnackbarMessage('Failed to submit request. Please try again.');
      setShowSnackbar(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loadingVehicles || loadingHistory) {
    return (
      <div className="p-6 flex items-center justify-center bg-gray-700" style={{ minHeight: "calc(100vh - 64px)" }}>
        <div className="text-center">
          <div className="w-48 h-48 mx-auto"> {/* Adjust size as needed */}
            <Lottie
              animationData={carAnimation}
              loop={true}
              autoplay={true}
            />
          </div>
          <p className="text-xl text-white">Loading roadside assistance...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-700 text-white p-6">
      <h1 className="text-2xl font-semibold mb-6 text-center">
        Roadside Assistance
      </h1>
      {/* Booked Vehicles */}
      <div className="bg-gray-900 p-6 rounded-md shadow-lg w-full max-w-6xl mx-auto mt-8">
        <h2 className="text-2xl font-semibold mb-6 text-center text-white">
          Booked Vehicles
        </h2>

        {loadingVehicles ? (
          <p className="text-center text-gray-400">
            Loading booked vehicles...
          </p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {bookedVehicles.length > 0 ? (
              bookedVehicles.map((bvehicle) => (
                <div
                  key={bvehicle.id}
                  className="bg-gray-800 p-4 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 cursor-pointer"
                  onClick={() => handleOpenModal(bvehicle.vehicle)}
                >
                  <img
                    src={bvehicle.vehicle.image_url}
                    alt={bvehicle.vehicle.model}
                    className="w-full h-40 object-cover rounded-md mb-4"
                  />
                  <div className="p-2">
                    <h3 className="text-lg font-semibold text-blue-400">
                      {`${bvehicle.vehicle.make} ${bvehicle.vehicle.model}`}
                    </h3>
                    <p className="text-gray-400 mt-2">
                      <strong>Fuel Type:</strong> {bvehicle.vehicle.fuel_type}
                    </p>
                    <p className="text-gray-400 mt-1">
                      <strong>Body Type:</strong> {bvehicle.vehicle.body_type}
                    </p>
                    <p className="text-gray-400 mt-1">
                      <strong>Year:</strong> {bvehicle.vehicle.year}
                    </p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-center col-span-full text-gray-400">
                No car is booked. Please book a car for this service.
              </p>
            )}
          </div>
        )}
      </div>
      {/*  Roadside Assistance History */}
      <div className="bg-gray-800 p-6 rounded-md shadow-md w-full max-w-6xl mx-auto mt-8">
        <h2 className="text-2xl font-semibold mb-4 text-center text-white">
          Roadside Assistance History
        </h2>

        {loadingHistory ? (
          <p className="text-center text-gray-400">
            Loading Roadside Assistance history...
          </p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {rsaHistory.length === 0 ? (
              <p className="text-gray-300 text-center col-span-full">
                No Roadside Assistance history available.
              </p>
            ) : (
              rsaHistory.map((service) => (
                <div
                  key={service.id}
                  className="bg-gray-700 rounded-lg shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105"
                >
                  <img
                    src={service.vehicle_details.image_url}
                    alt={`${service.vehicle_details.make} ${service.vehicle_details.model}`}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="text-lg font-semibold text-blue-400">
                      {service.vehicle_details.make}{" "}
                      {service.vehicle_details.model}
                    </h3>
                    <p className="text-gray-300 mt-2">
                      <strong>Location:</strong> {service.location}
                    </p>
                    <p className="text-gray-300 mt-2">
                      <strong>Provider:</strong>{" "}
                      {service.provider
                        ? "Assigned to " + service.provider
                        : "No provider assigned"}
                    </p>
                    <p className="text-gray-300 mt-2">
                      <strong>Service Type:</strong> {service.status}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
      {/* Appointment Scheduling Modal */}
      {selectedVehicle && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-gray-800 p-6 rounded-md shadow-md w-full max-w-lg relative">
            <button
              onClick={handleCloseModal}
              className="absolute top-2 right-2 text-gray-400 hover:text-white"
            >
              &times;
            </button>
            <h2 className="text-2xl font-semibold mb-4">
              {`${selectedVehicle.make} ${selectedVehicle.model}`}
            </h2>
            <img
              src={selectedVehicle.image_url}
              alt={selectedVehicle.model}
              className="w-full h-48 object-cover rounded-md mb-4"
            />
            <form onSubmit={handleAppointmentSubmit} className="space-y-4">
              <div>
                <label className="block text-gray-300 mb-2">Location</label>
                <input
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
                  placeholder="e.g., Bhubaneswar"
                  required
                />
              </div>

              <div>
                <label className="block text-gray-300 mb-2">Contact Number</label>
                <input
                  type="tel"
                  value={contactNumber}
                  onChange={(e) => setContactNumber(e.target.value)}
                  className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
                  placeholder="Enter your contact number"
                  required
                />
              </div>

              <div>
                <label className="block text-gray-300 mb-2">Assistance Type</label>
                <select
                  value={assistanceType}
                  onChange={(e) => setAssistanceType(e.target.value)}
                  className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
                  required
                >
                  <option value="">Select assistance type</option>
                  <option value="flat_tire">Flat Tire</option>
                  <option value="battery_jump">Battery Jump Start</option>
                  <option value="towing">Towing</option>
                  <option value="fuel_delivery">Fuel Delivery</option>
                  <option value="lockout">Others</option>
                </select>
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 p-3 rounded-md hover:bg-blue-700 transition"
                disabled={isSubmitting}
              >
                {isSubmitting ? "Submitting..." : "Request Assistance"}
              </button>
            </form>
          </div>
        </div>
      )}
      <Snackbar
        message={snackbarMessage}
        isVisible={showSnackbar}
        onClose={() => setShowSnackbar(false)}
      />
    </div>
  );
}

export default Page5;
