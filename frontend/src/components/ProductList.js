import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

function ProductList({ addToCart }) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

  const fetchProducts = useCallback(async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/products`);
      // Ensure response.data is an array
      const productsData = Array.isArray(response.data) ? response.data : [];
      setProducts(productsData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching products:', error);
      console.error('Error details:', error.response?.data || error.message);
      setProducts([]); // Set empty array on error
      setLoading(false);
    }
  }, [API_BASE_URL]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  const handleAddToCart = (productId) => {
    addToCart(productId, 1);
  };

  if (loading) {
    return <div className="card">Loading products...</div>;
  }

  // Ensure products is always an array before mapping
  if (!Array.isArray(products)) {
    return (
      <div>
        <h2>Products</h2>
        <div className="card">No products available. Please try again later.</div>
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <div>
        <h2>Products</h2>
        <div className="card">No products found.</div>
      </div>
    );
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
