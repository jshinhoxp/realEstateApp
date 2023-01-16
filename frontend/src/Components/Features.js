import React from 'react'

import { Routes, Route } from 'react-router-dom';
import Stocks from '../Pages/Stocks';
import News from '../Pages/News';
import Analyzer from '../Pages/Analyzer';
import Redirect from '../Components/Redirect';

function Features () { 
  return (
    <div>
    <Routes>
          <Route path="/" element={<Stocks />} />
          <Route path="/Stocks" element={<Stocks />} />
          <Route path="/News" element={<News />} />
          <Route path="/Analyzer" element={<Analyzer />} />
          <Route path="/external" element={<Redirect />} />
      </Routes>
      </div>
  )
}

export default Features