// src/Pages/HomePage.jsx
import HomeLayout from '../Layouts/HomeLayout';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <HomeLayout>
      <div className="bg-gray-700 min-h-screen p-8 text-white">
        <section className="bg-gray-800 p-6 rounded-md shadow-md mb-6">
          <div className="flex items-center justify-center mb-6">
            <img 
              src="src\assets\Images\SSO_Icons\image.png" 
              alt="AutoHub Logo" 
              className="h-20 w-auto"
            />
          </div>
          <h1 className="text-3xl font-bold mb-4 text-center">Welcome to AutoHub – Your Gateway to Smarter Vehicle Choices</h1>
          <p className="text-gray-300 text-center leading-relaxed">
            AutoHub provides a unified platform for discovering, comparing, and booking vehicles. With personalized recommendations tailored to your unique needs—whether it's fuel efficiency, eco-friendliness, or budget—AutoHub makes finding the perfect car easier than ever.
          </p>
        </section>

        <section className="bg-gray-800 p-6 rounded-md shadow-md mb-6">
          <h2 className="text-2xl font-bold mb-6">What We Offer</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="p-6 bg-gray-700 rounded-md hover:bg-gray-600 transition duration-300">
              <h3 className="text-xl font-semibold mb-3">Vehicle Catalog</h3>
              <p className="text-gray-300">Explore a diverse range of vehicles, from electric models to traditional favorites, and easily compare them to find the best fit.</p>
            </div>
            <div className="p-6 bg-gray-700 rounded-md hover:bg-gray-600 transition duration-300">
              <h3 className="text-xl font-semibold mb-3">Easy Test Drive & Booking</h3>
              <p className="text-gray-300">Schedule test drives or complete your purchase online or at a dealership—whatever is most convenient for you.</p>
            </div>
            <div className="p-6 bg-gray-700 rounded-md hover:bg-gray-600 transition duration-300">
              <h3 className="text-xl font-semibold mb-3">Comprehensive Support</h3>
              <p className="text-gray-300">Benefit from post-sale services, including maintenance scheduling, roadside assistance, and a direct feedback channel.</p>
            </div>
          </div>
        </section>

        <section className="bg-gray-800 p-8 rounded-md shadow-md text-center">
          <h2 className="text-2xl font-bold mb-4">AutoHub Makes Car Shopping Simple</h2>
          <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
            From discovery to purchase, AutoHub delivers a seamless, customer-centered experience tailored to today's drivers. Start exploring and see how easy it is to find your next vehicle with AutoHub by your side.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/login" 
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-md transition duration-300 ease-in-out"
            >
              Login
            </Link>
            <Link 
              to="/signup" 
              className="bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-8 rounded-md transition duration-300 ease-in-out"
            >
              Sign Up
            </Link>
          </div>
        </section>
      </div>
    </HomeLayout>
  );
};

export default HomePage;
