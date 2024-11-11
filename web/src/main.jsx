import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import App from './App.jsx'
import './index.css'
import store from './Redux/store.js'

import { getUserData } from './Redux/Slice/AuthSlice.js';

// Dispatch an action when the app starts
const token = localStorage.getItem('accessToken');
if (token) {
  // If an access token exists, verify if it's still valid (check expiry).
    store.dispatch(getUserData());
}
// else If the token is invalid (or doesn't exist), redirect to the login page.

createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <App />
  </Provider>
)
