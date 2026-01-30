import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/HomePage';
import { CartPage } from '../pages/CartPage';
import { CheckoutPage } from '../pages/CheckoutPage';

test.describe('Complete E2E Shopping Flow', () => {
  test('should complete full checkout process successfully', async ({ page }) => {
    // Initialize Page Objects
    const homePage = new HomePage(page);
    const cartPage = new CartPage(page);
    const checkoutPage = new CheckoutPage(page);

    // Step 1: Navigate to home page and verify products
    await homePage.navigate();
    await homePage.verifyPageLoaded();
    await homePage.verifyProductsDisplayed();
    
    const productCount = await homePage.getProductCount();
    expect(productCount).toBeGreaterThan(0);

    // Step 2: Add product to cart
    await homePage.addProductToCart('Laptop');
    
    // Verify cart count updated
    const cartCount = await homePage.getCartItemCount();
    expect(parseInt(cartCount)).toBeGreaterThan(0);

    // Step 3: Navigate to cart
    await homePage.clickCart();
    await cartPage.verifyOnCartPage();
    
    // Verify item in cart
    await cartPage.verifyItemInCart('Laptop');
    const itemCount = await cartPage.getItemCount();
    expect(itemCount).toBe(1);

    // Step 4: Proceed to checkout
    await cartPage.proceedToCheckout();
    await checkoutPage.verifyOnCheckoutPage();
    await checkoutPage.verifyOrderSummaryVisible();

    // Step 5: Fill checkout form
    await checkoutPage.fillCheckoutForm({
      email: 'test@example.com',
      shippingAddress: '123 Test Street, Test City, TC 12345',
      paymentMethod: 'credit_card',
      cardNumber: '4111111111111111',
      cardExpiry: '12/25',
      cvv: '123'
    });

    // Step 6: Place order
    await checkoutPage.placeOrder();
    
    // Verify success (order confirmation page)
    await expect(page.locator('text=Order Confirmed')).toBeVisible();
    await expect(page.locator('.order-number')).toBeVisible();
  });

  test('should apply discount code successfully', async ({ page }) => {
    const homePage = new HomePage(page);
    const cartPage = new CartPage(page);
    const checkoutPage = new CheckoutPage(page);

    // Add product and navigate to checkout
    await homePage.navigate();
    await homePage.addProductToCart('Laptop');
    await homePage.clickCart();
    await cartPage.proceedToCheckout();
    await checkoutPage.verifyOnCheckoutPage();

    // Get original total
    const originalTotal = await checkoutPage.getTotal();

    // Apply discount code
    await checkoutPage.applyDiscountCode('SAVE10');
    
    // Wait for discount to be applied
    await page.waitForTimeout(1000);
    
    // Verify discount applied
    const discountAmount = await checkoutPage.getDiscount();
    expect(discountAmount).not.toBe('$0.00');
    
    const newTotal = await checkoutPage.getTotal();
    expect(newTotal).not.toBe(originalTotal);
  });

  test('should handle multiple items in cart', async ({ page }) => {
    const homePage = new HomePage(page);
    const cartPage = new CartPage(page);

    await homePage.navigate();

    // Add multiple products
    await homePage.addProductToCart('Laptop');
    await homePage.addProductToCart('Mouse');
    await homePage.addProductToCart('Keyboard');

    // Navigate to cart
    await homePage.clickCart();
    await cartPage.verifyOnCartPage();

    // Verify all items present
    await cartPage.verifyItemInCart('Laptop');
    await cartPage.verifyItemInCart('Mouse');
    await cartPage.verifyItemInCart('Keyboard');

    const itemCount = await cartPage.getItemCount();
    expect(itemCount).toBe(3);
  });

  test('should update item quantity in cart', async ({ page }) => {
    const homePage = new HomePage(page);
    const cartPage = new CartPage(page);

    await homePage.navigate();
    await homePage.addProductToCart('Laptop');
    await homePage.clickCart();

    // Get initial quantity
    const initialQty = await cartPage.getItemQuantity('Laptop');
    expect(initialQty).toBe('1');

    // Update quantity
    await cartPage.updateItemQuantity('Laptop', 2);
    await page.waitForTimeout(1000);

    // Verify quantity updated
    const newQty = await cartPage.getItemQuantity('Laptop');
    expect(newQty).toBe('2');
  });

  test('should remove item from cart', async ({ page }) => {
    const homePage = new HomePage(page);
    const cartPage = new CartPage(page);

    await homePage.navigate();
    await homePage.addProductToCart('Mouse');
    await homePage.clickCart();

    // Verify item present
    await cartPage.verifyItemInCart('Mouse');

    // Remove item
    await cartPage.removeItem('Mouse');
    await page.waitForTimeout(1000);

    // Verify item removed
    await cartPage.verifyItemNotInCart('Mouse');
    
    // Verify cart is empty
    const isEmpty = await cartPage.isCartEmpty();
    expect(isEmpty).toBe(true);
  });

  test('should show validation errors for invalid email', async ({ page }) => {
    const homePage = new HomePage(page);
    const cartPage = new CartPage(page);
    const checkoutPage = new CheckoutPage(page);

    await homePage.navigate();
    await homePage.addProductToCart('Laptop');
    await homePage.clickCart();
    await cartPage.proceedToCheckout();

    // Fill with invalid email
    await checkoutPage.fillEmail('invalid-email');
    await checkoutPage.fillShippingAddress('123 Test St');
    await checkoutPage.selectPaymentMethod('credit_card');
    await checkoutPage.fillCardDetails('4111111111111111', '12/25', '123');

    // Try to place order
    await checkoutPage.placeOrder();

    // Verify error message
    await expect(page.locator('text=Invalid email')).toBeVisible();
  });

  test('should navigate between pages correctly', async ({ page }) => {
    const homePage = new HomePage(page);
    const cartPage = new CartPage(page);
    const checkoutPage = new CheckoutPage(page);

    // Home -> Cart
    await homePage.navigate();
    await homePage.clickCart();
    await cartPage.verifyOnCartPage();

    // Cart -> Checkout
    await homePage.addProductToCart('Laptop');
    await cartPage.proceedToCheckout();
    await checkoutPage.verifyOnCheckoutPage();

    // Checkout -> Cart
    await checkoutPage.backToCart();
    await cartPage.verifyOnCartPage();

    // Cart -> Home
    await cartPage.continueShopping();
    await homePage.verifyPageLoaded();
  });

  test('should persist cart across page refreshes', async ({ page }) => {
    const homePage = new HomePage(page);
    const cartPage = new CartPage(page);

    await homePage.navigate();
    await homePage.addProductToCart('Laptop');
    await homePage.clickCart();
    await cartPage.verifyItemInCart('Laptop');

    // Refresh page
    await page.reload();

    // Verify cart still has item
    await cartPage.verifyItemInCart('Laptop');
    const itemCount = await cartPage.getItemCount();
    expect(itemCount).toBe(1);
  });
});
