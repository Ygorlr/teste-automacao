from playwright.sync_api import sync_playwright
import pandas as pd


# Constantes
URL = "https://books.toscrape.com/"
GENRER = "Mystery"
EXCEL = "dados.xlsx"
RATING_STARS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

# Função extrair informações dos livros
def extract_details_books(page):
    title = page.locator(".product_main h1").inner_text()

    price = page.locator(".product_main p.price_color").inner_text()
    price = float(price.replace('£', ''))

    stars = page.locator(".product_main p.star-rating").get_attribute("class").split(" ")[1]
    stars = RATING_STARS.get(stars, 0)

    stock = int(page.locator(".product_main p.availability").inner_text().split("(")[1].split(" ")[0])

    description = page.locator("article.product_page > p")
    description = description.inner_text() if description.is_visible() else ""

    upc = page.locator("article.product_page table.table-striped tr").filter(has_text="UPC").locator("td").inner_text()

    return {
        "title": title,
        "price": price,
        "stars": stars,
        "stock": stock,
        "description": description,
        "upc": upc,
    }

# Função exportar em arquivo (.xlsx)
def save_excel(data):
    dataframe = pd.DataFrame(data)
    dataframe.to_excel(EXCEL, index=False)
    print(f"[3/4] Dados salvos com sucesso em: {EXCEL}")

# Função imprimir resumo no terminal
def print_terminal(total_books, total_value, total_qty_disp):
    print("=" * 40)
    print("[4/4] Resumo final:")
    print(f"    Total de livros: {total_books}")
    print(f"    Preço médio dos livros: £ {total_value/total_books:.2f}") if total_books > 0 else 0
    print(f"    Quantidade disponível total: {total_qty_disp}")
    print("=" * 40)

# Função principal
def main():
    data = []
    total_books = 0
    total_value = 0
    total_qty_disp = 0
    count_pag = 0

    with sync_playwright() as spw:
        browser = spw.chromium.launch()
        page = browser.new_page()
        page.goto(URL)

        try:
            page.get_by_role("link", name=GENRER, exact=True).click()
            print("[1/4] Página de 'Mystery'!")

            while True:
                page.locator("article.product_pod h3 > a").first.wait_for()
                count = page.locator("article.product_pod h3 > a").count()

                print(f"[2/4] Extraindo informações dos livros, pag({count_pag+1})...")

                for i in range(count):
                    page.locator("article.product_pod h3 > a").nth(i).click()
                    books = extract_details_books(page)

                    total_books += 1
                    total_value += books["price"]
                    total_qty_disp += books["stock"]

                    data.append({
                        "Título": books["title"],
                        "Preço": f"£ {books["price"]}",
                        "Estrelas": books["stars"],
                        "Estoque": books["stock"],
                        "Descrição": books["description"],
                        "UPC": books["upc"],
                    })
                    page.go_back()

                next_pag = page.get_by_role("link", name="next")
                if next_pag.is_visible():
                    next_pag.click()
                    count_pag += 1
                else:
                    break
            if data:
                save_excel(data)
            print_terminal(total_books, total_value, total_qty_disp)
            page.close()
            browser.close()
        except Exception as e:
            print(f"Ocorreu um erro durante a execução: {e}.")

if __name__ == "__main__":
    main()
