import React, { useState } from "react";
import HomeLayout from "../Layouts/HomeLayout";
import { useLocation } from "react-router-dom";
import axios from "axios";

function Page6() {
  const location = useLocation();
  const vehicleData = location.state.vehicle;
  return (
    <HomeLayout>
      <CarPurchasePage vehicle={vehicleData} />
    </HomeLayout>
  );
}

function CarPurchasePage({ vehicle }) {
  const [transactionId, setTransactionId] = useState("");
  const [isPurchasing, setIsPurchasing] = useState(false);
  const [purchaseStatus, setPurchaseStatus] = useState(null);

  const handlePurchase = () => {
    if (!transactionId) {
      alert("Please enter a transaction ID.");
      return;
    }

    setIsPurchasing(true);

    const user = localStorage.getItem("user");

    const userId = JSON.parse(user);

    const data = {
      vehicle_id: vehicle.id,
      user_name: userId.userName,
      transaction_id: transactionId,
    };

    // API call to purchase car
    axios
      .post("http://localhost:8003/bookings", data)
      .then((response) => {
        setPurchaseStatus(response.data.message || "Purchase successful!");
        setIsPurchasing(false);
      })
      .catch((error) => {
        console.error("Purchase error:", error);
        setPurchaseStatus("Purchase failed. Please try again.");
        setIsPurchasing(false);
      });
  };

  return (
    <div className="bg-gray-700 min-h-screen p-8 text-white">
      {/* Car Details Section */}
      <section className="bg-gray-800 p-6 rounded-md shadow-md mb-6">
        <img
          src={vehicle.image_url}
          alt={vehicle.model}
          className="w-full h-64 object-cover rounded-md mb-4"
        />
        <h3 className="text-2xl font-semibold">{vehicle.model}</h3>
        <p className="text-lg font-semibold text-gray-400 mb-2">
          Price: ${vehicle.price}
        </p>
        <p className="text-gray-400 mb-1">Fuel Type: {vehicle.fuel_type}</p>
        <p className="text-gray-400 mb-1">Body Type: {vehicle.body_type}</p>
        <p className="text-gray-400 mb-1">Year: {vehicle.year}</p>
        <p className="text-gray-400">Transmission: {vehicle.transmission}</p>
      </section>

      {/* Purchase Section */}
      <section className="bg-gray-800 p-6 rounded-md shadow-md">
        <h4 className="text-xl font-semibold mb-4">Complete Your Purchase</h4>
        <input
          type="text"
          placeholder="Enter Transaction ID"
          value={transactionId}
          onChange={(e) => setTransactionId(e.target.value)}
          className="w-full p-2 rounded-md bg-gray-900 text-white mb-4"
        />
        <button
          onClick={handlePurchase}
          disabled={isPurchasing}
          className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md w-full"
        >
          {isPurchasing ? "Processing..." : "Booking Confirm"}
        </button>
        {purchaseStatus && <p className="text-center mt-4">{purchaseStatus}</p>}
      </section>
    </div>
  );
}

export default Page6;
