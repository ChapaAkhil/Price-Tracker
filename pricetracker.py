import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import re

def get_price(url):
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Cache-Control': 'max-age=0'
        })
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: Received response code {response.status_code} for URL: {url}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Update this selector based on the actual website structure
        price_element = soup.select_one('.a-price-whole')  # Modify this as necessary
        
        if price_element:
            price_text = price_element.text.strip()
            price_number = re.findall(r'[\d,]+', price_text)
            if price_number:
                price = float(price_number[0].replace(',', ''))
                return price
        else:
            print("Price element not found in the page.")
            print("Page content for debugging:")
            print(soup.prettify())  # Output the full page content for analysis

        return None
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def send_email(subject, body, to_email, from_email, from_password):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, from_password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def track_price(url, target_price, to_email, from_email, from_password, check_interval, max_attempts=10):
    attempts = 0
    while attempts < max_attempts:
        current_price = get_price(url)
        if current_price is not None:
            print(f"Current Price: ₹{current_price}")
            if current_price <= target_price:
                subject = "Product Price Dropped!"
                body = f"The price dropped to ₹{current_price}!\nThis is below your target price of ₹{target_price}.\nCheck the product here: {url}"
                send_email(subject, body, to_email, from_email, from_password)
                break
            else:
                print("Price not yet low enough, checking again later.")
        else:
            print("Could not retrieve the current price, will try again.")

        attempts += 1
        print(f"Attempt {attempts}/{max_attempts}. Waiting for {check_interval} seconds...")
        time.sleep(check_interval)

    if attempts >= max_attempts:
        print("Max attempts reached. Exiting price tracker.")

if __name__ == "__main__":
    url = input("Enter the product URL: ")
    target_price = float(input("Enter your target price: "))
    check_interval = 3600  # Check every hour

    from_email = input("Enter your email: ")
    from_password = input("Enter your password: ")  # Consider using getpass for security
    to_email = input("Enter the recipient email: ")

    print("Starting price tracking...")
    try:
        track_price(url, target_price, to_email, from_email, from_password, check_interval)
    except KeyboardInterrupt:
        print("\nPrice tracking stopped by user.")
