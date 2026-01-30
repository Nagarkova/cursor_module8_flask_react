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
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    fetchCart();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const API_BASE_URL = 'http://localhost:5001';

  const fetchCart = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/cart?session_id=${sessionId}`);
      console.log(response.data);
      setCart(response.data);
    } catch (error) {
      console.error('Error fetching cart:', error);
    }
  };

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => {
      setNotification(null);
    }, 3000); // Auto-dismiss after 3 seconds
  };

  const addToCart = async (productId, quantity = 1) => {
    try {
      const result = await axios.post(`${API_BASE_URL}/api/cart/add`, {
        session_id: sessionId,
        product_id: productId,
        quantity: quantity
      });
      console.log(result.data);
      await fetchCart(); // Update cart immediately
      showNotification('Item added to cart successfully!', 'success');
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Failed to add item to cart';
      showNotification(errorMsg, 'error');
    }
  };

  const removeFromCart = async (itemId) => {
    try {
      await axios.post(`${API_BASE_URL}/api/cart/remove`, {
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
      await axios.post(`${API_BASE_URL}/api/cart/update`, {
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

      {notification && (
        <div className={`notification notification-${notification.type}`}>
          {notification.message}
        </div>
      )}

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
