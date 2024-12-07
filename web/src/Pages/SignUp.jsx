// src/Pages/Signup.jsx
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { registerUser } from "../Redux/Slice/AuthSlice"; // Ensure you have this action in your slice
import { toast } from "react-hot-toast";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [confirePassword, setConfirePassword] = useState("");
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    if (
      !username ||
      !email ||
      !password ||
      !confirePassword ||
      !phone ||
      !address ||
      !firstname ||
      !lastname
    ) {
      toast.error("All fields are required");
      return;
    }
    if (password !== confirePassword) {
      toast.error("Password does not match");
      return;
    }

    dispatch(
      registerUser({
        userName: username,
        email,
        password,
        firstName: firstname,
        lastName: lastname,
        phoneNumber: phone,
        address: address,
      })
    )
      .unwrap()
      .then(() => {
        toast.success("Registration successful!");
        // Optionally redirect or perform additional actions
        navigate("/login");
      })
      .catch((error) => {
        console.log(error.message);
        console.log(error.stack);

        toast.error("Registration failed: " + error.message);
      });
  };

  return (
    <div className="bg-gray-700 h-screen w-screen flex items-center justify-center">
      <div className="w-[90%] md:w-2/3 p-4 bg-gray-800 shadow-lg rounded-lg">
        <h1 className="text-2xl font-bold text-center text-white mb-8">
          Sign Up to AutoHub
        </h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              htmlFor="username"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              Username
            </label>
            <input
              type="text"
              id="username"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="password"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="confirePassword"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              confirm Password
            </label>
            <input
              type="Password"
              id="confirePassword"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={confirePassword}
              onChange={(e) => setConfirePassword(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          {/* ------------------------ */}
          <div className="mb-4">
            <label
              htmlFor="firstname"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              Firstname
            </label>
            <input
              type="text"
              id="firstname"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={firstname}
              onChange={(e) => setFirstname(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="lastname"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              Lastname
            </label>
            <input
              type="text"
              id="lastname"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={lastname}
              onChange={(e) => setLastname(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="phone"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              Phone
            </label>
            <input
              type="number"
              id="phone"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="address"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              Address
            </label>
            <input
              type="text"
              id="address"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              required
            />
          </div>
          {/* <div className="mb-4">
            <label
              htmlFor="password"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="confirePassword"
              className="block text-gray-300 text-sm font-bold mb-2"
            >
              confirm Password
            </label>
            <input
              type="Password"
              id="confirePassword"
              className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-700 text-white"
              value={confirePassword}
              onChange={(e) => setConfirePassword(e.target.value)}
              required
            />
          </div> */}
          <div className="flex items-center justify-center">
            <button
              type="submit"
              className="bg-indigo-500 text-white px-4 py-2 rounded-md hover:bg-indigo-600"
            >
              Sign Up
            </button>
          </div>
        </form>

        <div className="flex flex-col items-center justify-center mt-6">
          <Link to="/login" className="text-indigo-300 hover:underline">
            Already have an account? Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Signup;
