import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class CartPage extends BasePage {
  // Locators
  private readonly cartHeader: Locator;
  private readonly cartItems: Locator;
  private readonly emptyCartMessage: Locator;
  private readonly checkoutButton: Locator;
  private readonly totalAmount: Locator;
  private readonly continueShoppingButton: Locator;

  constructor(page: Page) {
    super(page);
    this.cartHeader = page.locator('h2:has-text("Shopping Cart")');
    this.cartItems = page.locator('.cart-item');
    this.emptyCartMessage = page.locator('text=Your cart is empty');
    this.checkoutButton = page.locator('button:has-text("Proceed to Checkout")');
    this.totalAmount = page.locator('.cart-total');
    this.continueShoppingButton = page.locator('button:has-text("Continue Shopping")');
  }

  // Actions
  async verifyOnCartPage() {
    await expect(this.cartHeader).toBeVisible();
  }

  async getItemCount(): Promise<number> {
    return await this.cartItems.count();
  }

  async isCartEmpty(): Promise<boolean> {
    return await this.emptyCartMessage.isVisible();
  }

  async getCartTotal(): Promise<string> {
    return await this.totalAmount.textContent() || '';
  }

  async getItemQuantity(productName: string): Promise<string> {
    const item = this.page.locator(`.cart-item:has-text("${productName}")`);
    return await item.locator('input[type="number"]').inputValue();
  }

  async updateItemQuantity(productName: string, quantity: number) {
    const item = this.page.locator(`.cart-item:has-text("${productName}")`);
    await item.locator('input[type="number"]').fill(quantity.toString());
    await this.waitForAPIResponse('/api/cart/update');
  }

  async removeItem(productName: string) {
    const item = this.page.locator(`.cart-item:has-text("${productName}")`);
    await item.locator('button:has-text("Remove")').click();
    await this.waitForAPIResponse('/api/cart/remove');
  }

  async proceedToCheckout() {
    await this.checkoutButton.click();
  }

  async continueShopping() {
    await this.continueShoppingButton.click();
  }

  async verifyItemInCart(productName: string) {
    const item = this.page.locator(`.cart-item:has-text("${productName}")`);
    await expect(item).toBeVisible();
  }

  async verifyItemNotInCart(productName: string) {
    const item = this.page.locator(`.cart-item:has-text("${productName}")`);
    await expect(item).not.toBeVisible();
  }
}
