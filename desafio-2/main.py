from playwright.sync_api import sync_playwright


URL = "https://www.saucedemo.com/"

# Função de capturar usuário e senha de acesso
def credentials(page):
    username = page.locator("[data-test='login-credentials']").inner_text().split("\n")[1]
    password = page.locator("[data-test='login-password']").inner_text().split("\n")[1]
    print("[1/9] Coletando credenciais de acesso")

    return {
        "username": username,
        "password": password,
    }

# Função realizar login
def login(page, username, password):
    page.locator("input[data-test='username']").fill(username)
    page.locator("input[data-test='password']").fill(password)
    page.locator("input[data-test='login-button']").click()

    print("[2/9] Realizando login")

# Função verificar carrinho
def verification_badge(page, i):
    badge_text = page.locator("[data-test='shopping-cart-badge']").inner_text()
    count = int(badge_text) if badge_text else 0
    print(f"[4/9] Produto {i+1} adicionado no carrinho!")

    return count

# Função finalizar compra
def checkout(page, firstname, lastname, postalcode):
    page.locator("[data-test='shopping-cart-link']").click()
    page.locator("[data-test='checkout']").click()
    print("[5/9] Confirmando carrinho!")

    # inserindo os dados
    page.locator("[data-test='firstName']").fill(firstname)
    page.locator("[data-test='lastName']").fill(lastname)
    page.locator("[data-test='postalCode']").fill(postalcode)
    print("[6/9] Dados da tela de informações preenchidos")

    page.locator("input[data-test='continue']").click()
    page.locator("[data-test='finish']").click()
    print("[7/9] Pagamento concluido!")

# Função de sair
def logout(page):
    page.get_by_role("button", name="Open Menu").click()
    page.locator("[data-test='logout-sidebar-link']").click()
    print("[8/9] Logout concluido!")   

# Função principal
def main():
    DATA = {
    "firstname": "Ygor",
    "lastname": "Rocha",
    "postalcode": "12345-678"
    }

    with sync_playwright() as spw:
        browser = spw.chromium.launch()
        page = browser.new_page()

        while True:
            page.goto(URL)

            credencial = credentials(page)
            login(page, credencial["username"], credencial["password"])

            page.locator("select[data-test='product-sort-container']").select_option("lohi")
            print("[3/9] Aplicando filtro 'Price (low to high)'")

            for i in range(3):
                page.get_by_role("button", name="Add to cart").nth(0).click()
                verification_badge(page, i)

            checkout(page, DATA["firstname"], DATA["lastname"], DATA["postalcode"])
            logout(page)

            if page.url == URL:
                print("[9/9] Tela de login! Loop encerrado com sucesso!")
                break

        browser.close()

if __name__ == "__main__":
    main()