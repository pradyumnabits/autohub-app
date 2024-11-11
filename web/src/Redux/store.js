// src/Redux/store.js
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './Slice/AuthSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    // Add other reducers if you have them
  },
});

export default store;
