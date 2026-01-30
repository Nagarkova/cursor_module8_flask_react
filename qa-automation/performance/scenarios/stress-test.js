import http from 'k6/http';
import { check, sleep } from 'k6';

// Stress test - gradually increase load to find breaking point
export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '3m', target: 100 },  // Ramp up to 100 users
    { duration: '2m', target: 150 },  // Ramp up to 150 users
    { duration: '3m', target: 200 },  // Ramp up to 200 users
    { duration: '2m', target: 0 },    // Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000'], // 95% under 3s
    http_req_failed: ['rate<0.10'],     // 10% error tolerance
  },
};

const API_URL = __ENV.API_URL || 'http://localhost:5001';

export default function () {
  const sessionId = `stress-${__VU}-${__ITER}`;

  // Simulate user workflow
  http.get(`${API_URL}/api/products`);
  sleep(1);

  http.post(
    `${API_URL}/api/cart/add`,
    JSON.stringify({
      session_id: sessionId,
      product_id: Math.floor(Math.random() * 4) + 1,
      quantity: 1,
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  sleep(2);

  http.get(`${API_URL}/api/cart?session_id=${sessionId}`);
  sleep(1);
}
