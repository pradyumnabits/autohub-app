// src/Redux/Slice/AuthSlice.js
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axiosInstance from "../../Helpers/axiosInstance.js";
import toast from "react-hot-toast";

export const registerUser = createAsyncThunk(
  "/auth/register",
  async (userData, { rejectWithValue }) => {
    try {
      const response = axiosInstance.post("/auth/register", userData);
      toast.promise(response, {
        loading: "Wait! creating your account...",
        success: (data) => {
          return data.data?.msg || "Account created successfully !";
        },
        error: "Failed to create account",
      });
      return (await response).data;
    } catch (error) {
      toast.error(error?.response?.data?.message);
      return rejectWithValue(error.response.data || "Registration failed !");
    }
  }
);

export const loginUser = createAsyncThunk(
  "auth/login",
  async (Credentials, { rejectWithValue }) => {
    try {
      const response = axiosInstance.post("auth/login", Credentials);
      console.log((await response).data);

      toast.promise(response, {
        loading: "Wait! Logging in...",
        success: (data) => {
          return data?.data?.message || "Logged in Successfully !";
        },
        error: "Failed to Login",
      });

      const { token, user } = (await response).data;

      // Store the access token in localStorage
      localStorage.setItem("accessToken", token);
      localStorage.setItem("user", JSON.stringify(user));

      // Set authorization header for future requests
      axiosInstance.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${token}`;

      return { user, accessToken: token };
    } catch (error) {
      console.log("I am ", error);
      toast.error(error["response"]["data"]["detail"]);
      return rejectWithValue(error.response.data || "Login failed !");
    }
  }
);

export const logout = createAsyncThunk("auth/logout", async () => {
  // Clear the access token from localStorage
  localStorage.removeItem("accessToken");
  delete axiosInstance.defaults.headers.common["Authorization"];
  toast.success("Logged out successfully");
});

export const getUserData = createAsyncThunk("auth/getUserData", async () => {
  try {
    // const res = await axiosInstance.get("user/me");
    // return res.data; // Assumes the API response contains user data

    // Instead of calling the real API, return mock data
    const mockUserData = {
      user: {
        username: "testUser",
        email: "testuser@example.com",
        role: "admin", // Or any role you want to test
      },
    };

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500));

    return mockUserData; // Return mock data
  } catch (error) {
    toast.error(error.response?.data?.message || "Failed to fetch user data");
    throw error;
  }
});

export const getUserProfile = createAsyncThunk(
  "auth/getUserProfile",
  async (_, { getState, rejectWithValue }) => {
    const { token } = getState().auth;

    if (!token) return rejectWithValue("No token available");

    try {
      const response = await axiosInstance.get("user/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const authSlice = createSlice({
  name: "auth",
  initialState: {
    isLoggedIn: false,
    role: "",
    data: {},
    accessToken: localStorage.getItem("token") || null,
  },
  reducers: {},
  extraReducers: (builder) => {
    // Handle Login
    builder
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoggedIn = true;
        state.data = action?.payload?.user;
        state.accessToken = action?.payload?.access_Token;
        state.role = action?.payload?.user?.role;
        console.log(action?.payload);
      })
      .addCase(logout.fulfilled, (state) => {
        state.isLoggedIn = false;
        state.data = {};
        state.role = "";
        state.accessToken = null;
      })
      .addCase(getUserData.fulfilled, (state, action) => {
        state.data = action.payload.user; // Update user data
      })
      .addCase(getUserProfile.rejected, (state, action) => {
        state.isLoggedIn = false;
        localStorage.removeItem("token");
        toast.error("Session expired. Please log in again.");
      });
  },
});

// Action creators are generated for each case reducer function
export const {} = authSlice.actions;

export default authSlice.reducer;
