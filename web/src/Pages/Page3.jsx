import React, { useState } from "react";
import HomeLayout from "../Layouts/HomeLayout";
import { useLocation } from "react-router-dom";
import axios from "axios";
import { AllUrl } from "../Helpers/allUrl";
// this page is to book test drive
function Page3() {
  const location = useLocation();
  const vehicleData = location.state.vehicle;
  return (
    <HomeLayout>
      <TestDriveBooking vehicle={vehicleData} />
    </HomeLayout>
  );
}

function TestDriveBooking({ vehicle }) {
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [loading, setLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e) => {
    const user = localStorage.getItem("user");

    const userId = JSON.parse(user);
    console.log(userId.userName);

    e.preventDefault();
    setLoading(true);
    const data = {
      vehicle_id: vehicle.id,
      user_name: userId.userName,
      date,
      time,
    };
    axios
      .post(`${AllUrl.bookingServiceUrl}/testdrives/book`, data)
      .then((res) => {
        console.log(res);

        setLoading(false);
        setIsSubmitted(true);
      })
      .catch((err) => {
        console.log(err);

        setLoading(false);
        console.error(err);
      });
  };

  const handleClose = () => {
    setIsSubmitted(false);

    setDate("");
    setTime("");
  };

  return (
    <div className="min-h-screen bg-gray-700 text-white flex items-center justify-center p-6">
      <div className="bg-gray-800 p-6 rounded-md shadow-md w-full max-w-lg">
        <h1 className="text-2xl font-semibold mb-6 text-center">
          Book a Test Drive
        </h1>

        {/* Booking Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="bg-gray-900 p-4 rounded-md mb-2 shadow-md">
            <h5 className="text-lg font-semibold">Selected Vehicle</h5>
            <div className="flex items-center">
              <img
                src={vehicle.image_url}
                alt="Vehicle Image"
                className="w-20 h-20 mr-4"
              />
              <div>
                <p className="text-gray-300">Model: {vehicle.model}</p>
                <p className="text-gray-300">Make: {vehicle.make}</p>
                <p className="text-gray-300">Price: ₹{vehicle.price}</p>
                <p className="text-gray-300">Type: {vehicle.body_type}</p>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-gray-300 mb-2">Select Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
              min={new Date().toISOString().split("T")[0]} // Sets the minimum date to today
              required
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-2">Select Time</label>
            <input
              type="time"
              value={time}
              onChange={(e) => setTime(e.target.value)}
              className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 p-3 rounded-md mt-4 hover:bg-blue-700 transition"
          >
            {loading ? "Loading..." : "Confirm Booking"}
          </button>
        </form>
      </div>

      {/* Confirmation Modal */}
      {isSubmitted && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-80 flex items-center justify-center p-4">
          <div className="bg-gray-800 p-6 rounded-md shadow-md w-full max-w-md text-center">
            <div className="checkmark-container mb-4">
              <div className="checkmark-icon"></div>
            </div>
            <h2 className="text-xl font-semibold text-white mb-2">
              Booking Confirmed!
            </h2>
            <p className="text-gray-300 mb-6">
              Your test drive for {vehicle.model} is booked on {date} at {time}.
            </p>
            <button
              onClick={handleClose}
              className="bg-blue-600 px-4 py-2 rounded-md hover:bg-blue-700 transition"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
export default Page3;
