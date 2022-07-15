import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import { Footer, Header, Faq } from './Bases';
import Home from './Home';
import Checkout from './Checkout';

import 'bootstrap-icons/font/bootstrap-icons.css';
import Shipping from './Shipping';
import { CardPayment, TransferPayment, Payment } from './Payment';

class App extends React.Component {
  render() {
    return (
      <Router>
        <div>
          <Header />
          <Routes>
            <Route exact path='/' element={<Home />} />
            <Route exact path='/faq' element={<Faq />} />
            <Route exact path='/cardpayment' element={<CardPayment />} />
            <Route exact path='/checkout'  element={<Checkout />} />
            <Route exact path='/shipping' element={<Shipping />} />
            <Route exact path='/payment' element={<Payment />} />
            <Route exact path='/cardpayment' element={<CardPayment />} />
            <Route exact path='/transferpayment' element={<TransferPayment />} />
          </Routes>
          <div className="border rounded" id="spinner"></div> 
          <Footer />
        </div>
      </Router>
    )
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
