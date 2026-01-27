import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ProductList({ addToCart }) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get('/api/products');
      setProducts(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching products:', error);
      setLoading(false);
    }
  };

  const handleAddToCart = (productId) => {
    addToCart(productId, 1);
  };

  if (loading) {
    return <div className="card">Loading products...</div>;
  }

  return (
    <div>
      <h2>Products</h2>
      <div className="product-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <h3>{product.name}</h3>
            <div className="price">${product.price.toFixed(2)}</div>
            <div className="description">{product.description}</div>
            <div className="stock">In Stock: {product.stock}</div>
            <button
              className="btn btn-primary"
              onClick={() => handleAddToCart(product.id)}
              disabled={product.stock === 0}
            >
              {product.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProductList;
