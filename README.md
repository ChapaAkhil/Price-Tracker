# Price Tracker

This project is a Python-based price tracker that monitors the price of a product from an online store and sends an email notification when the price drops below a specified target.

## Features
- Fetches the current price of a product from a given URL.
- Sends email notifications when the price drops below the user-specified target.
- Configurable check interval and retry attempts.
- Uses `BeautifulSoup` for web scraping and `smtplib` for email notifications.

---

## Prerequisites

Ensure you have the following installed:
1. Python 3.x
2. Required Python libraries:
   - requests
   - bs4 (BeautifulSoup)
   - smtplib
   - re

Install missing libraries using:
```bash
pip install requests beautifulsoup4
