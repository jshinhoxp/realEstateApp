import React from 'react';

import "./css/App.css"
// Import react components below
import Navbar from './Components/Navbar';
import Footer from './Components/Footer';
import Features from './Components/Features';

// <> is the short syntax for fragments
function App() {
  return (
    <div className="page-container">
        <div className="content-wrapper">
          <Navbar />
          <Features />
          <Footer />
        </div>
    </div>
  )
}
export default App;
