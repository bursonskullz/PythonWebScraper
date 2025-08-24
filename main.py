import tkinter as tk
from tkinter import ttk
from scrapModule import scraper

def main():
    root = tk.Tk()
    root.title("PriceWebScraper")
    root.geometry("1000x700")
    root.configure(bg="#f0f2f5")
    root.resizable(True, True)

    main_frame = tk.Frame(root, bg="#f0f2f5")
    main_frame.pack(fill="both", expand=True)
    sidebar = tk.Frame(main_frame, bg="#f0f2f5", width=200)
    sidebar.pack(side="left", fill="y")

    tk.Label(
        sidebar,
        text="Websites",
        bg="#2c3e50",
        fg="white",
        font=("Helvetica", 11, "bold"),
        pady=10
    ).pack(fill="x", padx=10)

    websites = scraper.load_endpoints()

    website_tree = ttk.Treeview(
        sidebar,
        columns=("Website",),
        show="tree",
        height=20,
        style="Professional.Treeview"
    )

    website_tree.column("#0", width=150)

    current_stores = scraper.initilizeStores(websites, website_tree);
    website_tree.pack(pady=5, padx=10, fill="x")
    search_frame = tk.Frame(main_frame, bg="#f0f2f5")
    search_frame.pack(fill="x", padx=25, pady=10)

    search_entry = tk.Entry(
        search_frame,
        font=("Helvetica", 12),
        relief="flat",
        bg="white",
        bd=1,
        width=55
    )
    search_entry.pack(side="left", pady=5, ipady=5, padx=(0, 5))
    search_entry.insert(0, "Search for products...")

    search_entry.bind("<FocusIn>", lambda event: scraper.clear_placeholder(event, search_entry))

    results_frame = tk.Frame(main_frame, bg="#f0f2f5")
    results_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("Product", "Price", "Website", "Link")
    tree = ttk.Treeview(
        results_frame,
        columns=columns,
        show="headings",
        style="Professional.Treeview"
    )
    tree.heading("Product", text="Product")
    tree.heading("Price", text="Price (USD)")
    tree.heading("Website", text="Website")
    tree.heading("Link", text="Link")
    tree.pack(side="left", fill="both", expand=True)

    search_button = tk.Button(
        search_frame,
        text="🔍 Search",
        command=lambda: scraper.perform_search(search_entry.get(), status_label, progress_bar, recommended_label, current_stores, websites, tree),
        bg="#2c3e50",
        fg="white",
        font=("Helvetica", 10, "bold"),
        relief="flat",
        activebackground="#2980b9",
        cursor="hand2"
    )
    search_button.pack(side="left", pady=5)

    progress_bar = ttk.Progressbar(
        search_frame,
        mode="indeterminate",
        length=100,
        style="Professional.Horizontal.TProgressbar"
    )

    status_label = tk.Label(
        main_frame,
        text="",
        bg="#f0f2f5",
        fg="#e74c3c",
        font=("Helvetica", 10)
    )
    status_label.pack(fill="x", padx=20, pady=5)

    recommended_frame = tk.Frame(main_frame, bg="#ecf0f1", relief="groove", bd=2)
    recommended_frame.pack(fill="x", padx=20, pady=10)
    tk.Label(
        recommended_frame,
        text="Recommended Option",
        bg="#ecf0f1",
        fg="#2c3e50",
        font=("Helvetica", 11, "bold"),
        pady=5
    ).pack(anchor="w", padx=10)

    recommended_label = tk.Label(
        recommended_frame,
        text="No recommendation yet",
        bg="#ecf0f1",
        fg="#7f8c8d",
        font=("Helvetica", 10),
        wraplength=700,
        anchor="w",
        justify="left"
    )
    recommended_label.pack(fill="x", padx=10, pady=5)

    y_scroll = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
    y_scroll.pack(side="right", fill="y")
    tree.configure(yscrollcommand=y_scroll.set)

    #tree.bind("<Double-1>", lambda event: scraper.open_link(event))

    logo_frame = tk.Frame(main_frame, bg="#f0f2f5")
    logo_frame.pack(expand=True)
    logo_canvas = tk.Canvas(logo_frame, bg="#f0f2f5", highlightthickness=0)
    logo_canvas.pack(pady=20)

    logo_canvas.create_text(
        102, 52,  
        text="WebScraper",
        font=("Montserrat", 24, "bold"),  
        fill="#7f8c8d",  
        anchor="center"
    )

    logo_canvas.create_text(
        100, 50,  
        text="WebScraper",
        font=("Montserrat", 24, "bold"), 
        fill="#3498db",  
        anchor="center"
    )

    root.bind("<Configure>", lambda event: scraper.resize_columns(event, tree))
    scraper.resize_columns(None, tree)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Professional.TMenubutton",
        background="#2c3e50",
        foreground="white",
        font=("Helvetica", 10),
        padding=5
    )
    style.configure(
        "Professional.Treeview",
        background="white",
        foreground="#2c3e50",
        rowheight=25,
        fieldbackground="white"
    )
    style.configure(
        "Professional.Treeview.Heading",
        background="#2c3e50",
        foreground="white",
        font=("Helvetica", 10, "bold")
    )

    style.configure(
        "Professional.Horizontal.TProgressbar",
        troughcolor="#f0f2f5",
        background="#3498db",
        thickness=20
    )

    style.map(
        "Professional.Treeview",
        background=[
            ("selected", "white"),
            ("!selected", "white"),
            ("active", "white")
        ],
        foreground=[
            ("selected", "#2c3e50"),
            ("!selected", "#2c3e50"),
            ("active", "#2c3e50")
        ]
    )
    style.map(
        "Professional.Treeview.Heading",
        background=[
            ("active", "#2c3e50"),
            ("!active", "#2c3e50")
        ],
        foreground=[
            ("active", "white"),
            ("!active", "white")
        ]
    )

    search_entry.bind("<Return>", lambda event: scraper.perform_search(search_entry.get(), status_label, progress_bar, recommended_label, current_stores, websites, tree))
    tree.bind("<<TreeviewSelect>>", lambda event: scraper.update_logo_visibility(tree, logo_frame))
    root.mainloop()

if __name__ == "__main__":
    main()
