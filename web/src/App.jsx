import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./Pages/HomePage";
import Login from "./Pages/Login";
import SignUp from "./Pages/SignUp";
import Dashboard from "./Pages/Page1";
import Page2 from "./Pages/Page2";
import Page3 from "./Pages/Page3";
import Page4 from "./Pages/Page4";
import Page5 from "./Pages/Page5";
import Page6 from "./Pages/Page6";
import Page7 from "./Pages/Page7";

import { Toaster } from "react-hot-toast";
const App = () => {
  return (
    // <>
    //   Ram Ram
    // </>
    <>
      <Router>
        <Toaster />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/catalog" element={<Page2 />} />
          <Route path="/testdrivebook" element={<Page3 />} />
          <Route path="/support" element={<Page4 />} />
          <Route path="/rsa" element={<Page5 />} />
          <Route path="/book" element={<Page6 />} />
          <Route path="/feedbackp" element={<Page7 />} />

        </Routes>
      </Router>
    </>
  );
};

export default App;
