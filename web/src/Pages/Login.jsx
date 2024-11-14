// src/Pages/Login.jsx
import { useState } from "react";
import { useDispatch } from "react-redux";
import { loginUser } from "../Redux/Slice/AuthSlice";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      toast.error("Please fill all the details!");
      return;
    }
    setLoading(true); //Disable the button on submit
    try {
      const loginResponse = await dispatch(
        loginUser({ userName: username, password })
      );
      console.log("Login response: ", loginResponse.type);

      if (loginResponse["payload"]["user"] != null) {
        setPassword("");
        setUsername("");
        navigate("/dashboard");
        console.log("Thanks");
      }
    } catch (error) {
      console.log("Login failed: ", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="bg-gray-700 h-screen w-screen flex items-center justify-center">
      <div className="w-[90%] md:w-2/3 p-4 bg-gray-800 shadow-lg rounded-lg">
        <h1 className="text-2xl font-bold text-center text-white mb-8">
          Login to AutoHub
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
              onChange={(e) => setUsername(e.target.value)}
              value={username}
              disabled={loading}
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
              onChange={(e) => setPassword(e.target.value)}
              value={password}
              disabled={loading}
            />
          </div>
          <div className="flex items-center justify-center">
            <button
              type="submit"
              className="bg-indigo-500 text-white px-4 py-2 rounded-md hover:bg-indigo-600"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </div>
        </form>

        {/* SSO Section */}
        <div className="text-center text-gray-400">------OR------</div>
        <div className="text-center text-gray-400">Login With</div>
        <div className="flex items-center justify-center my-6">
          <div className="flex space-x-4">
            {/* Google Button */}
            <button className="bg-gray-700 border border-gray-600 rounded-full p-2 shadow-md hover:shadow-lg transition duration-300">
              <img
                src="src/assets/Images/SSO_Icons/Google.png"
                alt="Google"
                className="w-8 h-8"
              />
            </button>

            {/* Microsoft Button */}
            <button className="bg-gray-700 border border-gray-600 rounded-full p-2 shadow-md hover:shadow-lg transition duration-300">
              <img
                src="src/assets/Images/SSO_Icons/Microsoft.png"
                alt="Microsoft"
                className="w-8 h-8"
              />
            </button>

            {/* Facebook Button */}
            <button className="bg-gray-700 border border-gray-600 rounded-full p-2 shadow-md hover:shadow-lg transition duration-300">
              <img
                src="src/assets/Images/SSO_Icons/Facebook.png"
                alt="Facebook"
                className="w-8 h-8"
              />
            </button>
          </div>
        </div>
        <div className="flex flex-col items-center justify-center">
          <Link
            to="/forgot-password"
            className="text-indigo-300 hover:underline"
          >
            Forgot password?
          </Link>
          <Link to="/signup" className="text-indigo-300 hover:underline">
            Sign Up ?
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
