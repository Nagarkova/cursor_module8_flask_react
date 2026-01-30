import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
  // Locators
  private readonly header: Locator;
  private readonly productsButton: Locator;
  private readonly cartButton: Locator;
  private readonly productList: Locator;
  private readonly productCards: Locator;
  private readonly cartCount: Locator;

  constructor(page: Page) {
    super(page);
    this.header = page.locator('h1:has-text("E-Commerce Checkout")');
    this.productsButton = page.locator('button:has-text("Products")');
    this.cartButton = page.locator('button:has-text("Cart")');
    this.productList = page.locator('.product-list');
    this.productCards = page.locator('.product-card');
    this.cartCount = page.locator('.cart-count');
  }

  // Actions
  async navigate() {
    await super.navigate('/');
    await this.waitForPageLoad();
  }

  async verifyPageLoaded() {
    await expect(this.header).toBeVisible();
    await expect(this.productsButton).toBeVisible();
  }

  async clickProducts() {
    await this.productsButton.click();
  }

  async clickCart() {
    await this.cartButton.click();
  }

  async getProductCount(): Promise<number> {
    await this.productList.waitFor();
    return await this.productCards.count();
  }

  async getCartItemCount(): Promise<string> {
    return await this.cartCount.textContent() || '0';
  }

  async searchProduct(productName: string): Promise<Locator> {
    return this.page.locator(`.product-card:has-text("${productName}")`);
  }

  async addProductToCart(productName: string) {
    const product = await this.searchProduct(productName);
    await product.locator('button:has-text("Add to Cart")').click();
    await this.waitForAPIResponse('/api/cart/add');
  }

  async getProductPrice(productName: string): Promise<string> {
    const product = await this.searchProduct(productName);
    return await product.locator('.price').textContent() || '';
  }

  async isProductInStock(productName: string): Promise<boolean> {
    const product = await this.searchProduct(productName);
    const button = product.locator('button:has-text("Add to Cart")');
    return await button.isEnabled();
  }

  async verifyProductsDisplayed() {
    await expect(this.productList).toBeVisible();
    const count = await this.getProductCount();
    expect(count).toBeGreaterThan(0);
  }
}
