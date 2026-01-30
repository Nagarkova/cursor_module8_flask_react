import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class CheckoutPage extends BasePage {
  // Locators
  private readonly checkoutHeader: Locator;
  private readonly emailInput: Locator;
  private readonly shippingAddressInput: Locator;
  private readonly paymentMethodSelect: Locator;
  private readonly cardNumberInput: Locator;
  private readonly cardExpiryInput: Locator;
  private readonly cardCVVInput: Locator;
  private readonly discountCodeInput: Locator;
  private readonly applyDiscountButton: Locator;
  private readonly orderSummary: Locator;
  private readonly subtotal: Locator;
  private readonly discount: Locator;
  private readonly total: Locator;
  private readonly placeOrderButton: Locator;
  private readonly backToCartButton: Locator;

  constructor(page: Page) {
    super(page);
    this.checkoutHeader = page.locator('h2:has-text("Checkout")');
    this.emailInput = page.locator('input[name="email"]');
    this.shippingAddressInput = page.locator('textarea[name="shipping_address"]');
    this.paymentMethodSelect = page.locator('select[name="payment_method"]');
    this.cardNumberInput = page.locator('input[name="card_number"]');
    this.cardExpiryInput = page.locator('input[name="card_expiry"]');
    this.cardCVVInput = page.locator('input[name="cvv"]');
    this.discountCodeInput = page.locator('input[name="discount_code"]');
    this.applyDiscountButton = page.locator('button:has-text("Apply")');
    this.orderSummary = page.locator('.order-summary');
    this.subtotal = page.locator('.subtotal');
    this.discount = page.locator('.discount');
    this.total = page.locator('.total');
    this.placeOrderButton = page.locator('button:has-text("Place Order")');
    this.backToCartButton = page.locator('button:has-text("Back to Cart")');
  }

  // Actions
  async verifyOnCheckoutPage() {
    await expect(this.checkoutHeader).toBeVisible();
  }

  async fillEmail(email: string) {
    await this.emailInput.fill(email);
  }

  async fillShippingAddress(address: string) {
    await this.shippingAddressInput.fill(address);
  }

  async selectPaymentMethod(method: string) {
    await this.paymentMethodSelect.selectOption(method);
  }

  async fillCardDetails(cardNumber: string, expiry: string, cvv: string) {
    await this.cardNumberInput.fill(cardNumber);
    await this.cardExpiryInput.fill(expiry);
    await this.cardCVVInput.fill(cvv);
  }

  async applyDiscountCode(code: string) {
    await this.discountCodeInput.fill(code);
    await this.applyDiscountButton.click();
    await this.waitForAPIResponse('/api/discount/apply');
  }

  async getSubtotal(): Promise<string> {
    return await this.subtotal.textContent() || '';
  }

  async getDiscount(): Promise<string> {
    return await this.discount.textContent() || '';
  }

  async getTotal(): Promise<string> {
    return await this.total.textContent() || '';
  }

  async placeOrder() {
    await this.placeOrderButton.click();
    await this.waitForAPIResponse('/api/checkout');
  }

  async backToCart() {
    await this.backToCartButton.click();
  }

  async fillCheckoutForm(data: {
    email: string;
    shippingAddress: string;
    paymentMethod: string;
    cardNumber: string;
    cardExpiry: string;
    cvv: string;
  }) {
    await this.fillEmail(data.email);
    await this.fillShippingAddress(data.shippingAddress);
    await this.selectPaymentMethod(data.paymentMethod);
    await this.fillCardDetails(data.cardNumber, data.cardExpiry, data.cvv);
  }

  async verifyOrderSummaryVisible() {
    await expect(this.orderSummary).toBeVisible();
  }
}
