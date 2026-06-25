import json
from playwright.sync_api import sync_playwright


URL = "https://demoqa.com/automation-practice-form"
FILE_IMAGE = "image.png"
FILE_JSON = "data.json"
SAVE_SCREENSHOT = "saida/confirmation.png"
CALENDAR = {
    "Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
    "May": "May", "Jun": "June", "Jul": "July", "Aug": "August", 
    "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December"
}

# Função para abrir o arquivo (.json)
def open_json():
    with open(FILE_JSON, "r", encoding="utf-8") as file:
        return json.load(file)

# Função para inserir os dados no formulário
def submit_form(page, data_file, first_name, last_name, email, phone, date):
    # inserir no formulário nome, sobrenome e email 
    page.locator("#firstName").fill(first_name)
    page.locator("#lastName").fill(last_name)
    page.locator("#userEmail").fill(email)

    # inserir no formulário gênero, número de telefone, data de nascimento
    page.locator(f"#genterWrapper input[value='{data_file['gender']}']").check()
    page.locator("#userNumber").fill(phone)
    page.locator("#dateOfBirth input").fill(date)

    # inserir no formulário Hobby
    for hobby in data_file["hobbies"]:
        page.locator(f"label:has-text('{hobby}')").click()

    # inserir no formulário imagem
    page.locator("#uploadPicture").set_input_files(FILE_IMAGE)

    # Botão de enviar formulário
    page.get_by_role("button", name="Submit").click()
    print("[1/4] Dados submetidos com sucesso!")

# Função para salvar as informações da tela modal
def data_modal(page, data):
    page.wait_for_selector(".table-responsive")
    linhas = page.locator(".table-responsive tr").all()
    for linha in linhas:
        cel = linha.locator("td").all_inner_texts()
        if len(cel) == 2:
            data[cel[0]] = cel[1]
    return data

# Função para comparar os dados
def assert_modal(page, data_file):
    data = {}
    data_modal(page, data)

    # asserção e tratamento Nome
    full_name = f"{data_file['first_name']} {data_file['last_name']}"
    try:
        assert full_name in data.get('Student Name', '')
    except AssertionError:
        print(f"Nome incorreto no modal: {data.get('Student Name')}")

    # asserção email
    try:
        assert data_file['email'] in data.get('Student Email', '')
    except AssertionError:
        print(f"Email incorreto no modal: {data.get('Student Email')}")

    # asserção gênero
    try:
        assert data_file['gender'] in data.get('Gender', '')
    except AssertionError:
        print(f"Gênero incorreto no modal: {data.get('Gender')}")

    # asserção número de telefone
    try:
        assert data_file['phone'] in data.get('Mobile', '')
    except AssertionError:
        print(f"Telefone incorreto no modal: {data.get('Mobile')}")

    # asserção e tratamento para data de nascimento
    date_format = data_file['date'].split(" ")
    day = date_format[0]
    month = date_format[1]
    year = date_format[2]
    date_format = f"{day} {CALENDAR.get(month, month)},{year}"
    try:
        assert date_format in data.get('Date of Birth', '')
    except AssertionError:
        print(f"Data de aniversário incorreta no modal: {data.get('Date of Birth')}")

    # asserção hobby
    try:
        hobbies_str = ", ".join(data_file["hobbies"])
        assert hobbies_str == data.get('Hobbies', '')
    except AssertionError:
        print(f"Hobby incorreto no modal: {data.get('Hobbies')}")
        print(hobbies_str)
        print(data.get('Hobbies'))

    print("[2/4] Validação do modal concluída com sucesso!")

# Função para capturar a tela modal
def screenshot_modal(page):
    try:
        screen_modal = page.locator(".modal-content")
        screen_modal.screenshot(path=SAVE_SCREENSHOT)
    except Exception:
        print("Não foi possível fazer a captura screenshot da tela modal")

    print("[3/4] Captura screenshot do modal realizada sucesso!")

# Função para enviar formulário vazio
def submit_empty(page):
    required_fields = page.locator("input[required]").all()
    print("[4/4] Lista de campos inválidos quando o formulário é submetido vazio: ", end='')
    for i in required_fields:
        print(f"{i.get_attribute('name') or i.get_attribute('id')}", end=', ')

# Função principal
def main():
    with sync_playwright() as spw:
        browser = spw.chromium.launch()
        page = browser.new_page()
        page.goto(URL)

        # arquivo (data.json) com os dados para inserir no formulário
        data_file = open_json()
        
        # Função para inserir os dados
        submit_form(
            page,
            data_file,
            data_file["first_name"],
            data_file["last_name"],
            data_file["email"],
            data_file["phone"],
            data_file["date"],
        )

        # Função para comparar os dados
        assert_modal(page, data_file)

        # Função para capturar a tela modal
        screenshot_modal(page)

        # Função para enviar formulário vazio
        submit_empty(page)

        browser.close()

if __name__ == "__main__":
    main()