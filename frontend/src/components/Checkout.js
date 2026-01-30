import React, { useState } from 'react';
import axios from 'axios';

function Checkout({ sessionId, cart, onSuccess, onBack }) {
  const [formData, setFormData] = useState({
    email: '',
    payment_method: 'card',
    card_number: '',
    cvv: '',
    expiry_date: '',
    shipping_address: '',
    discount_code: ''
  });
  const [discount, setDiscount] = useState(null);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Clear error when user starts typing
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: '' });
    }
  };

  const applyDiscount = async () => {
    if (!formData.discount_code) {
      setErrors({ ...errors, discount_code: 'Please enter a discount code' });
      return;
    }

    try {
      const response = await axios.post('http://localhost:5001/api/discount/apply', {
        session_id: sessionId,
        code: formData.discount_code
      });
      setDiscount(response.data);
      setErrors({ ...errors, discount_code: '' });
    } catch (error) {
      setErrors({
        ...errors,
        discount_code: error.response?.data?.error || 'Invalid discount code'
      });
      setDiscount(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    try {
      const checkoutData = {
        session_id: sessionId,
        email: formData.email,
        payment_method: formData.payment_method,
        shipping_address: formData.shipping_address,
        discount_code: formData.discount_code || null
      };

      if (formData.payment_method === 'card') {
        checkoutData.card_number = formData.card_number;
        checkoutData.cvv = formData.cvv;
        checkoutData.expiry_date = formData.expiry_date;
      }

      const response = await axios.post('http://localhost:5001/api/checkout', checkoutData);
      onSuccess(response.data);
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Checkout failed';
      setErrors({ submit: errorMessage });
    } finally {
      setLoading(false);
    }
  };

  const finalTotal = discount ? discount.final_total : cart.total;

  return (
    <div>
      <h2>Checkout</h2>
      <div className="card">
        <div className="cart-summary">
          <h3>Order Summary</h3>
          {cart.items.map(item => (
            <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span>{item.product_name} x {item.quantity}</span>
              <span>${item.subtotal.toFixed(2)}</span>
            </div>
          ))}
          {discount && (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px', color: '#28a745' }}>
                <span>Discount ({discount.discount_code}):</span>
                <span>-${discount.discount_amount.toFixed(2)}</span>
              </div>
            </>
          )}
          <div className="total">
            <span>Total:</span>
            <span>${finalTotal.toFixed(2)}</span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="checkout-form">
          <div className="discount-section">
            <label>Discount Code (Optional)</label>
            <div style={{ display: 'flex', gap: '10px' }}>
              <input
                type="text"
                name="discount_code"
                value={formData.discount_code}
                onChange={handleChange}
                placeholder="Enter discount code"
                style={{ flex: 1, margin: 0 }}
              />
              <button type="button" className="btn btn-secondary" onClick={applyDiscount}>
                Apply
              </button>
            </div>
            {errors.discount_code && <div className="error">{errors.discount_code}</div>}
            {discount && <div className="success">Discount applied successfully!</div>}
          </div>

          <label>Email Address *</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          {errors.email && <div className="error">{errors.email}</div>}

          <label>Shipping Address *</label>
          <textarea
            name="shipping_address"
            value={formData.shipping_address}
            onChange={handleChange}
            required
            rows="3"
            style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}
          />
          {errors.shipping_address && <div className="error">{errors.shipping_address}</div>}

          <label>Payment Method *</label>
          <select
            name="payment_method"
            value={formData.payment_method}
            onChange={handleChange}
            required
          >
            <option value="card">Credit/Debit Card</option>
            <option value="paypal">PayPal</option>
          </select>

          {formData.payment_method === 'card' && (
            <>
              <label>Card Number *</label>
              <input
                type="text"
                name="card_number"
                value={formData.card_number}
                onChange={handleChange}
                placeholder="1234 5678 9012 3456"
                maxLength="19"
                required
              />
              {errors.card_number && <div className="error">{errors.card_number}</div>}

              <div className="form-row">
                <div>
                  <label>CVV *</label>
                  <input
                    type="text"
                    name="cvv"
                    value={formData.cvv}
                    onChange={handleChange}
                    placeholder="123"
                    maxLength="4"
                    required
                  />
                  {errors.cvv && <div className="error">{errors.cvv}</div>}
                </div>
                <div>
                  <label>Expiry Date *</label>
                  <input
                    type="text"
                    name="expiry_date"
                    value={formData.expiry_date}
                    onChange={handleChange}
                    placeholder="MM/YY"
                    maxLength="5"
                    required
                  />
                  {errors.expiry_date && <div className="error">{errors.expiry_date}</div>}
                </div>
              </div>
            </>
          )}

          {errors.submit && <div className="error">{errors.submit}</div>}

          <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
            <button type="button" className="btn btn-secondary" onClick={onBack}>
              Back to Cart
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Processing...' : 'Place Order'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Checkout;
