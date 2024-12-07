// src/Components/Helpers/axiosInstance.js
import axios from "axios";
import { AllUrl } from "./allUrl";

const axiosInstance = axios.create({
  baseURL: AllUrl.authServiceUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
