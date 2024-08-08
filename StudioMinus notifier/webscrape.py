
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Discord Webhook URL
webhook_url = "https://discord.com/api/webhooks/ numbers here"

def scrape_and_send():
    # Create a new instance of the Firefox browser
    driver = webdriver.Firefox()

    try:
        # Navigate to the webpage with the blog posts
        driver.get("https://www.studiominus.nl/blog/index.html")

        # Wait for the articles to load
        time.sleep(1)  # Adjust the delay as needed

        # Find the link to the latest blog post
        latest_blog_link = driver.find_element(By.CLASS_NAME, "article-button").get_attribute("href")

        # Read the previous link from the text file
        previous_link = None
        try:
            with open("latestbloglink.txt", "r") as file:
                previous_link = file.read().strip()  # Remove leading/trailing whitespace
        except FileNotFoundError:
            pass

        # Print the latest blog link
        print("Latest blog link:", latest_blog_link)
        print("Previous blog link:", previous_link)

        # Compare the latest link with the previous one
        if previous_link is not None and latest_blog_link != previous_link:
            print("New blog link found. Sending to Discord...")

            # Send the latest blog link to Discord
            payload = {
                "content": f"<@& numbers here > {latest_blog_link}"
            }
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                print("Successfully sent to Discord")
            else:
                print(f"Failed to send to Discord with status code {response.status_code}")

            # Update the text file with the latest blog link
            with open("latestbloglink.txt", "w") as file:
                file.write(latest_blog_link)
                print("Updated text file with the latest blog link")
        else:
            print("No new blog link to send")

    finally:
        # Close the browser
        driver.quit()

# Run the scraping loop
while True:
    scrape_and_send()
    time.sleep(60)  # Repeat every X seconds
