from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import random
from PIL import Image

item = 'DESCENSOR' # Exemplo de item

# Processos para funcionar:
# - Mude a variável para o nome que foi informado pelo superior
# - É necessário que existe uma pasta dentro de "DOWNLOADS" com o mesmo nome de que está na variável "item"
# - Nessa pasta é necessário pelo menos 3 imagens com pelo menos 400x400 pixels
# - Download de extensões: "pip install selenium webdriver_manager pillow"

downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads", item)

if not os.path.exists(downloads_folder):
    raise Exception(f"A pasta {downloads_folder} não existe.")

image_files = [f for f in os.listdir(downloads_folder) if os.path.isfile(os.path.join(downloads_folder, f))]

valid_images = []
for image_file in image_files:
    try:
        with Image.open(os.path.join(downloads_folder, image_file)) as img:
            if img.width >= 400 and img.height >= 400:
                valid_images.append(image_file)
    except Exception as e:
        print(f"Erro ao abrir a imagem {image_file}: {e}")

if len(valid_images) < 3:
    raise Exception(f"A pasta {downloads_folder} deve conter pelo menos 3 imagens com pelo menos 400x400 pixels.")

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = 'url do site em questão'

driver.get(url)

username = "usuário para acessar o site em questão"
password = "senha para acessar o site em questão"

wait = WebDriverWait(driver, 10) # aguarda carregamento da página

# Buscar e preencher campos de usuário e senha 
username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

username_field.send_keys(username)
password_field.send_keys(password)

# Dar submit no formulário forçando a key "RETURN" (enter) no último campo do formulário
password_field.send_keys(Keys.RETURN)

driver.implicitly_wait(10)

# Busca pela tabela principal que aparece na página
table = wait.until(EC.presence_of_element_located((By.ID, "table_id")))

# Busca uma linha específica da tabela
row = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[td[contains(text(), 'valor de dentro da tabela')]]")))

# Se encontrar
if row:
    # Busque e clique no botão de iniciar processo
    link = row.find_element(By.XPATH, ".//a[contains(text(), 'Iniciar')]")
    if link:
        link.click()
        driver.implicitly_wait(10)
        while True:
            try:
                # Dentro de uma nova tabela busca por um item específico (variável item)
                table = driver.find_elements(By.TAG_NAME, "table")[0]

                item_row = table.find_element(By.XPATH, f".//tr[td[contains(text(), '{item}')]]")

                # ao achar clica no <a> (redirecionador) do item para o lugar desejado
                if item_row:
                    last_td = item_row.find_elements(By.TAG_NAME, "td")[-1]
                    link = last_td.find_element(By.TAG_NAME, "a")
                    if link:
                        link.click()

                        ct_button = wait.until(EC.presence_of_element_located((By.NAME, "ct_button")))
                        ct_button.click()

                        # Inicia o processo principal ("verificar" o equipamento)
                        classificacao_select = wait.until(EC.presence_of_element_located((By.ID, "select2-classificacao-container")))
                        classificacao_select.click()

                        classificacao_select_option = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'Média alteração')]")))
                        classificacao_select_option.click()

                        marca_select = wait.until(EC.presence_of_element_located((By.NAME, "marca")))

                        for option in marca_select.find_elements(By.TAG_NAME, 'option'):
                            if option.text == "Outro":
                                option.click()
                                break

                        other_marca_input = wait.until(EC.presence_of_element_located((By.NAME, "other_marca")))

                        other_marca_input.send_keys("Outro")

                        modelo_select = wait.until(EC.presence_of_element_located((By.NAME, "modelo")))

                        for option in modelo_select.find_elements(By.TAG_NAME, 'option'):
                            if option.text == "Outro":
                                option.click()
                                break

                        other_modelo_input = wait.until(EC.presence_of_element_located((By.NAME, "other_modelo")))

                        other_modelo_input.send_keys("Outro")

                        n_patrimonio_novo_input = wait.until(EC.presence_of_element_located((By.NAME, "n_patrimonio_novo")))

                        n_patrimonio_novo_value = n_patrimonio_novo_input.get_attribute("value")

                        serie_chassi_input = wait.until(EC.presence_of_element_located((By.NAME, "serie_chassi")))

                        serie_chassi_input.send_keys(n_patrimonio_novo_value)

                        file1_input = wait.until(EC.presence_of_element_located((By.ID, "file1")))
                        file2_input = wait.until(EC.presence_of_element_located((By.ID, "file2")))

                        # Dentro da pasta downloads busca pelas imagens e insere nos inputs (aleatoriza as imagens e escolhe duas)
                        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads", item)

                        files = [os.path.join(downloads_folder, f) for f in os.listdir(downloads_folder) if os.path.isfile(os.path.join(downloads_folder, f))]

                        valid_files = []
                        for file in files:
                            try:
                                with Image.open(file) as img:
                                    if img.width >= 400 and img.height >= 400:
                                        valid_files.append(file)
                            except Exception as e:
                                print(f"Erro ao abrir a imagem {file}: {e}")

                        if valid_files:
                            file_path = random.choice(valid_files)
                        else:
                            raise Exception(f"Nenhuma imagem válida encontrada na pasta {item}")

                        file1_input.send_keys(file_path)
                        file2_input.send_keys(file_path)

                        btn_caract = wait.until(EC.presence_of_element_located((By.ID, "btn_caract")))

                        btn_caract.click()

                        driver.implicitly_wait(10)
                    else:
                        print("Link dentro do último <td> não encontrado.")
                else:
                    print(f"Linha com '{item}' não encontrada.")
            except Exception as e:
                print(f"Erro: {e}")
                break
    else:
        print("Link 'Iniciar' não encontrado.")
else:
    print("Item 'item que deveria ser clicado' não encontrado.")