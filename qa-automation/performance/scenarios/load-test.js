import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp up to 20 users
    { duration: '1m', target: 20 },   // Stay at 20 users
    { duration: '30s', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests should be below 2s
    http_req_failed: ['rate<0.05'],     // Error rate should be less than 5%
    errors: ['rate<0.1'],               // Custom error rate should be less than 10%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';
const API_URL = __ENV.API_URL || 'http://localhost:5001';

export default function () {
  // Test 1: Load homepage
  let res = http.get(BASE_URL);
  check(res, {
    'homepage loaded': (r) => r.status === 200,
    'homepage has content': (r) => r.body.includes('E-Commerce'),
  }) || errorRate.add(1);

  sleep(1);

  // Test 2: Get products
  res = http.get(`${API_URL}/api/products`);
  check(res, {
    'products API success': (r) => r.status === 200,
    'products returned': (r) => {
      try {
        const products = JSON.parse(r.body);
        return Array.isArray(products) && products.length > 0;
      } catch {
        return false;
      }
    },
  }) || errorRate.add(1);

  sleep(1);

  // Test 3: Add to cart
  const sessionId = `session-${__VU}-${__ITER}`;
  res = http.post(
    `${API_URL}/api/cart/add`,
    JSON.stringify({
      session_id: sessionId,
      product_id: 1,
      quantity: 1,
    }),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );
  check(res, {
    'add to cart success': (r) => r.status === 201,
  }) || errorRate.add(1);

  sleep(1);

  // Test 4: Get cart
  res = http.get(`${API_URL}/api/cart?session_id=${sessionId}`);
  check(res, {
    'get cart success': (r) => r.status === 200,
    'cart has items': (r) => {
      try {
        const cart = JSON.parse(r.body);
        return cart.items && cart.items.length > 0;
      } catch {
        return false;
      }
    },
  }) || errorRate.add(1);

  sleep(2);
}
