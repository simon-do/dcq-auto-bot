import puppeteer from "puppeteer";
import "dotenv/config";
import { browserOptions } from "../../../core/browser/browserOptions.js";

const URL = process.env.DCQ_URL ?? "";
const USERNAME = process.env.DCQ_USERNAME ?? "";
const PASSWORD = process.env.DCQ_PASSWORD ?? "";

const run = async () => {
  // Launch the browser and open a new blank page.
  const browser = await puppeteer.launch(browserOptions);
  const page = await browser.newPage();

  // Navigate the page to a URL.
  await page.goto(URL);

  // Type into username and password input.
  await page.locator("#loginAccountInput").fill(USERNAME);
  await page.locator("#loginPassInput").fill(PASSWORD);

  // Click on login button.
  await page.locator("button.j-account-login-btn").click();

  // await browser.close();
};

run();
