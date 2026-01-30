
function Cart({ cart, removeFromCart, updateCartQuantity, onCheckout }) {
  if (cart.items.length === 0) {
    return (
      <div className="card">
        <h2>Your Cart</h2>
        <p>Your cart is empty.</p>
      </div>
    );
  }

  return (
    <div>
      <h2>Your Cart</h2>
      <div className="card">
        {cart.items.map(item => (
          <div key={item.id} className="cart-item">
            <div className="cart-item-info">
              <h4>{item.product_name}</h4>
              <div className="price">${item.price.toFixed(2)} each</div>
            </div>
            <div className="cart-item-controls">
              <input
                type="number"
                min="1"
                value={item.quantity}
                onChange={(e) => updateCartQuantity(item.id, parseInt(e.target.value))}
              />
              <div>${item.subtotal.toFixed(2)}</div>
              <button
                className="btn btn-danger"
                onClick={() => removeFromCart(item.id)}
              >
                Remove
              </button>
            </div>
          </div>
        ))}
        <div className="cart-summary">
          <div className="total">
            <span>Total:</span>
            <span>${cart.total.toFixed(2)}</span>
          </div>
          <button className="btn btn-primary" onClick={onCheckout}>
            Proceed to Checkout
          </button>
        </div>
      </div>
    </div>
  );
}

export default Cart;
