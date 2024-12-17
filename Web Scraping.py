import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product information
def scrape_products(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch the webpage. Status Code:", response.status_code)
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    products = []

    # Modify the selectors below based on the e-commerce site you choose
    for item in soup.find_all("div", class_="product-card"):
        name = item.find("h2", class_="product-title").get_text(strip=True) if item.find("h2", class_="product-title") else "N/A"
        price = item.find("span", class_="product-price").get_text(strip=True) if item.find("span", class_="product-price") else "N/A"
        rating = item.find("span", class_="product-rating").get_text(strip=True) if item.find("span", class_="product-rating") else "N/A"

        products.append({"Name": name, "Price": price, "Rating": rating})

    return products

# Function to save data to a CSV file
def save_to_csv(filename, products):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Price", "Rating"])
        writer.writeheader()
        writer.writerows(products)
    print("Data saved to", filename)

if __name__ == "__main__":
    # Example e-commerce website URL (replace with the site you want to scrape)
    url = "https://example.com/products"

    print("Scraping product data...")
    product_data = scrape_products(url)

    if product_data:
        save_to_csv("products.csv", product_data)
    else:
        print("No products found or failed to scrape.")
