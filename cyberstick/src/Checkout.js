import React from 'react';
import axios from 'axios';
import { Navigate } from 'react-router-dom';
import NumberFormat from 'react-number-format'; 


import { Steps, ScrollToTopOnMount, CheckoutForm } from './Bases';
import './static/Checkout.scss';
import cybersticbent from './static/cyberstickbent.png';

import $ from 'jquery';

const delivery_date = new Date(new Date().getTime()+(10*24*60*60*1000));

export default class Checkout extends React.Component {
    constructor(props) {
        $('#spinner').removeClass('hidden');
        sessionStorage.removeItem('PIP');
        super(props);
        this.state = {
            product_id: 1,    
            amount: 1,
            price: 25000,
            shipping: 'Free',
            tax: '-',
            color: 'Black',
            total_price: 25000,
            delivery_date: delivery_date.toDateString(),
            askinfo: false,
        };
    }

    clearCart = () => {
        sessionStorage.clear();
        this.setState({amount: 1, price: 25000, total_price: 25000})
    }

    componentDidMount() {
        $('#spinner').addClass('hidden');
        if (sessionStorage.getItem('amount')) {
            const amount = Number(sessionStorage.getItem('amount'))
            this.setState((prevState) => (
                {'amount': amount, price: prevState.price * amount, total_price: prevState.price * amount}
            )) 
        } else {
            this.setState({'amount': 1})
        }        
    }

    componentDidUpdate() {
        if (!this.state.askinfo)    
            sessionStorage.setItem('amount', this.state.amount)
    }    

    componentWillUnmount() {
        $('#spinner').removeClass('hidden');
    }    

    decreaseAmount = () => {
        if (this.state.amount > 1 && !this.state.askinfo)
            this.setState((prevState) => ({amount: prevState.amount - 1, price: prevState.price - 25000,
            total_price: prevState.total_price - 25000}))
    }    

    increaseAmount = () => {
        if (!this.state.askinfo)    
        this.setState((prevState) => ({amount: prevState.amount + 1, price: prevState.price + 25000,
            total_price: prevState.total_price + 25000}))
    }

    placeOrder = () => {
        $('#spinner').removeClass('hidden');
        if (this.state.amount > 0 && !this.state.askinfo) {
        axios.post('https://cyberstick-project.herokuapp.com/cyberstick/orders/', {    
        //axios.post('http://127.0.0.1:8000/cyberstick/orders/', {    
            id: this.state.product_id,
            amount: this.state.amount,
            total_price: this.state.total_price,
            color: this.state.color,
        })
        .then((res) => {
            sessionStorage.setItem('order_token', res['data']['Available'])
            sessionStorage.setItem('amount', res['data']['amount'])
            sessionStorage.removeItem('new_customer')
            sessionStorage.removeItem('customer')
            this.setState({askinfo: true})
        })
        .catch((err) => {alert('an error occured'); $('#spinner').addClass('hidden');});
    }
    }
    
    render() {
        if (this.state.askinfo) {
            return <Navigate to='/shipping' state={{shipping: this.state.shipping,
                tax: this.state.tax, total_price: this.state.total_price}}
            />
        }
        return (
            <div>
                <ScrollToTopOnMount />
                <div className='container-fluid'>
                <section className='row checkout-section-1
                justify-content-around align-items-center g-0px'>
                    <div className='col-md-6 col-12 aside-1'>
                        <h3>Review Your Bag.</h3>
                        <div className='d-flex align-items-center
                        justify-content-start flex-wrap py-3'>
                            <img className='cyberstickbent' src={cybersticbent} alt='product'/>
                            <div>
                                <p className='checkout-p my-1'>Cyberstick - {this.state.color}</p>
                                <p className='checkout-p my-1'>Get it By {this.state.delivery_date}</p>
                            </div>
                            <span className='amount px-3'>{this.state.amount}</span>
                            <div className='d-flex flex-column amount-controls'>
                                <i className='bi-caret-up increase' onClick={this.increaseAmount}></i>
                                <i className='bi-caret-down decrease' onClick={this.decreaseAmount}></i>
                            </div>
                            <div className='d-flex flex-column align-items-start
                            justify-content-center price-wrapper'>
                                <p className='checkout-p price my-1'><NumberFormat value={this.state.price}
                            displayType={'text'} thousandSeparator={true} prefix={'₦'} /></p>
                            <p className='checkout-p remove my-1' onClick={this.clearCart}>Remove</p>
                            </div>
                        </div>
                    </div>
                    <div className='col-md-4 col-12 aside-2 d-flex flex-column'>
                        <CheckoutForm header="order summary" price={this.state.price}
                        shipping={this.state.shipping} tax={this.state.tax} total_price={this.state.total_price}
                        />                   
                        <button className='checkout-btn' 
                        onClick={this.placeOrder} type='submit' value='Checkout'>Checkout</button>
                    </div>
                </section>
                </div>
                <Steps />
            </div>
            )
    }    
}
