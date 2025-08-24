import requests
import tkinter as tk
import random  
import json

class scraper:

    def load_endpoints():
        endpoints = 'endpoints.json'
        try:
            with open(endpoints, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def clear_placeholder(event, search_entry):
        if search_entry.get() == "Search for products...":
            search_entry.delete(0, tk.END)

    def resize_columns(event=None, tree = None):
        total_width = tree.winfo_width() - 20
        if total_width <= 0:
            return
        column_ratios = {
            "Product": 0.40,
            "Price": 0.15,
            "Website": 0.15,
            "Link": 0.30
        }
        for col, ratio in column_ratios.items():
            tree.column(col, width=int(total_width * ratio))

    def update_logo_visibility(tree, logo_frame):
        if tree.get_children():
            logo_frame.pack_forget()
        else:
            logo_frame.pack(expand=True)

    def perform_search(query, status_label, progress_bar, recommended_label, current_stores, websites, tree):
        if not query or query == "Search for products...":
            status_label.config(text="Please enter a search query")
            return
        print(f"Search query: '{query}' across all websites")
        status_label.config(text=f"Searching for '{query}' across all websites...")
        progress_bar.pack(side="left", padx=5)
        progress_bar.start()

        for item in tree.get_children():
            tree.delete(item)
        recommended_label.config(text="No recommendation yet")

        sample_results = []

        for website_name, items in current_stores:
            for item in items:
                if isinstance(item, dict) and 'title' in item and query.lower() in item['title'].lower():
                    title = item.get('title', 'Unknown Product')
                    price = item.get('price', round(random.uniform(1, 100), 2))  # Fallback to random price
                    try:
                        price = float(price)
                    except (ValueError, TypeError):
                        price = round(random.uniform(1, 100), 2)
                    link = item.get('link', 'No link available')
                    treeTuple = (title, price, website_name, link)
                    sample_results.append(treeTuple)

        if "Open Library" in websites:
            try:
                response = requests.get(websites["Open Library"] + query, timeout=5)
                response.raise_for_status()
                data = response.json().get("docs", [])
                for item in data:
                    if isinstance(item, dict) and 'title' in item and query.lower() in item['title'].lower():
                        title = item.get('title', 'Unknown Book')
                        price = round(random.uniform(1, 100), 2)  # Assign random price
                        link = f"https://openlibrary.org{item.get('key', '')}" if item.get('key') else "No link available"
                        treeTuple = (title, price, "Open Library", link)
                        sample_results.append(treeTuple)
            except (requests.RequestException, ValueError) as e:
                print(f"Error fetching Open Library data: {e}")

        for result in sample_results:
            tree.insert("", tk.END, values=result)

        if sample_results:
            recommended = min(sample_results, key=lambda x: x[1])  # All prices are numeric
            recommended_label.config(
                text=f"Product: {recommended[0]}\nPrice: {recommended[1]:.2f}\nWebsite: {recommended[2]}\nLink: {recommended[3]}"
            )
        else:
            recommended_label.config(text="No results found")

        progress_bar.stop()
        progress_bar.pack_forget()
        status_label.config(text="Search complete")
        return sample_results

    def initilizeStores(websites, website_tree): 
        store = []
        for name, url in websites.items():
            website_tree.insert("", tk.END, text=name)
            if name == "Open Library":
                continue  
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                if isinstance(data, dict):
                    data = [data]
                elif not isinstance(data, list):
                    print(f"Unexpected data format for {name}: {type(data)}")
                    continue
                for item in data:
                    if name == "Fake Store" and "id" in item:
                        item["link"] = f"https://fakestoreapi.com/products/{item['id']}"
                    elif name == "JSON PlaceHolder" and "id" in item:
                        item["link"] = f"https://jsonplaceholder.typicode.com/todos/{item['id']}"
                        item["price"] = round(random.uniform(1, 100), 2) 
                    else:
                        item["link"] = "No link available"
                        item["price"] = round(random.uniform(1, 100), 2)
                store.append((name, data))
                return store
            except (requests.RequestException, ValueError) as e:
                print(f"Error fetching data from {name}: {e}")
                return []

