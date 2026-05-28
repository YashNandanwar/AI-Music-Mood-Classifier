import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import './index.css';

function App() {
  return (
    <div className="app">
      <Navbar />
      <Home />
      <Footer />
    </div>
  );
}

export default App;
