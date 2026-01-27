import React from 'react';

function OrderConfirmation({ order }) {
  return (
    <div className="card order-confirmation">
      <h2>Order Confirmed!</h2>
      <p>Thank you for your order.</p>
      <div className="order-number">Order Number: {order.order_number}</div>
      <div style={{ marginTop: '20px' }}>
        <p><strong>Status:</strong> {order.status}</p>
        <p><strong>Total Amount:</strong> ${order.total_amount.toFixed(2)}</p>
      </div>
      <p style={{ marginTop: '20px', color: '#666' }}>
        A confirmation email has been sent to your email address.
      </p>
    </div>
  );
}

export default OrderConfirmation;
