import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import ProductList from './components/ProductList';
import Cart from './components/Cart';
import Checkout from './components/Checkout';
import OrderConfirmation from './components/OrderConfirmation';

function App() {
  const [sessionId] = useState(() => {
    // Generate or retrieve session ID
    let id = localStorage.getItem('sessionId');
    if (!id) {
      id = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('sessionId', id);
    }
    return id;
  });

  const [currentView, setCurrentView] = useState('products');
  const [cart, setCart] = useState({ items: [], total: 0, item_count: 0 });
  const [order, setOrder] = useState(null);

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await axios.get(`/api/cart?session_id=${sessionId}`);
      setCart(response.data);
    } catch (error) {
      console.error('Error fetching cart:', error);
    }
  };

  const addToCart = async (productId, quantity = 1) => {
    try {
      await axios.post('/api/cart/add', {
        session_id: sessionId,
        product_id: productId,
        quantity: quantity
      });
      await fetchCart();
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to add item to cart');
    }
  };

  const removeFromCart = async (itemId) => {
    try {
      await axios.post('/api/cart/remove', {
        session_id: sessionId,
        item_id: itemId
      });
      await fetchCart();
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to remove item');
    }
  };

  const updateCartQuantity = async (itemId, quantity) => {
    try {
      await axios.post('/api/cart/update', {
        session_id: sessionId,
        item_id: itemId,
        quantity: quantity
      });
      await fetchCart();
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to update cart');
    }
  };

  const handleCheckoutSuccess = (orderData) => {
    setOrder(orderData);
    setCurrentView('confirmation');
    fetchCart(); // Refresh cart (should be empty)
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>E-Commerce Checkout</h1>
        <nav>
          <button onClick={() => setCurrentView('products')}>Products</button>
          <button onClick={() => setCurrentView('cart')}>
            Cart ({cart.item_count})
          </button>
        </nav>
      </header>

      <main className="container">
        {currentView === 'products' && (
          <ProductList addToCart={addToCart} />
        )}
        {currentView === 'cart' && (
          <Cart
            cart={cart}
            removeFromCart={removeFromCart}
            updateCartQuantity={updateCartQuantity}
            onCheckout={() => setCurrentView('checkout')}
          />
        )}
        {currentView === 'checkout' && (
          <Checkout
            sessionId={sessionId}
            cart={cart}
            onSuccess={handleCheckoutSuccess}
            onBack={() => setCurrentView('cart')}
          />
        )}
        {currentView === 'confirmation' && order && (
          <OrderConfirmation order={order} />
        )}
      </main>
    </div>
  );
}

export default App;
