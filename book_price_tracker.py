import os
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Base URL for all pages
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

# Initialize list for all book data
all_books = []

# Loop through all 50 pages
for page in range(1, 51):
    url = base_url.format(page)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        break  # if we reach a broken link, stop
    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").get_text(strip=True)
        rating = book.p["class"][1]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_books.append([timestamp, title, price, rating])

# Create DataFrame
df = pd.DataFrame(all_books, columns=["Timestamp", "Title", "Price", "Rating"])

# Save to CSV
filename = "book_price_tracker.csv"
if os.path.exists(filename):
    df.to_csv(filename, mode='a', header=False, index=False)
else:
    df.to_csv(filename, index=False)

# Show output
print(f"✅ Total books scraped: {len(df)}")
print(df.head())
