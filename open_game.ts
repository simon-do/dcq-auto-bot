import puppeteer from "puppeteer";
import "dotenv/config";

const USERNAME = process.env.DCQ_USERNAME ?? "";
const PASSWORD = process.env.DCQ_PASSWORD ?? "";

const run = async () => {
  // Launch the browser and open a new blank page.
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--window-size=500,1000", "--window-position=0,0"],
    defaultViewport: {
      width: 500,
      height: 900,
    },
  });
  const page = await browser.newPage();

  // Navigate the page to a URL.
  await page.goto("https://h5.dcqvn.com/dcq?cid=363&isMobile=1");

  // Type into username and password input.
  await page.locator("#loginAccountInput").fill(USERNAME);
  await page.locator("#loginPassInput").fill(PASSWORD);

  // // Click on login button.
  await page.locator("button.j-account-login-btn").click();

  // await browser.close();
};

run();
