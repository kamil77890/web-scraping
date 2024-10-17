import time
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
gecko_driver_path = r"C:\Users\kamil\Downloads\geckodriver-v0.35.0-win64\geckodriver.exe"


def scrap_olx(q):
    # Ustawienia Firefoxa (headless, bez GUI)
    firefox_options = Options()
    # Możesz usunąć ten wiersz, jeśli chcesz widzieć, co się dzieje
    firefox_options.add_argument("--headless")

    # Ścieżka do GeckoDriver
    # Upewnij się, że ścieżka jest poprawna

    # Inicjalizacja przeglądarki
    service = Service(gecko_driver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        # Otwórz stronę OLX
        url = f"https://www.olx.pl/oferty/q-{q}/"
        driver.get(url)

        # Poczekaj na załadowanie przycisku akceptacji cookies
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="accept-cookie-banner"]'))
        )

        # Kliknij przycisk akceptacji cookies
        consent_button = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="accept-cookie-banner"]')
        consent_button.click()
        print("Akceptacja cookies zakończona.")

        # Czekaj dłużej na załadowanie wyników wyszukiwania
        time.sleep(5)  # Możesz dostosować ten czas

        # Pobierz HTML strony po załadowaniu wyników
        page_source = driver.page_source

        # Debugging: Wyświetl HTML
        print("HTML po akceptacji cookies:")
        print(page_source[:1000])  # Wyświetl pierwsze 1000 znaków HTML

        # Przetwarzanie HTML za pomocą BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Znajdź wszystkie elementy z wynikami
        # Dostosuj selektor w zależności od struktury HTML
        results = soup.select('div.offer-wrapper')

        # Sprawdzenie liczby znalezionych wyników
        print(f"Liczba znalezionych wyników: {len(results)}")

        for result in results:
            try:
                # Dostosuj selektor w zależności od struktury HTML
                title = result.find('h3').text.strip()
                link = result.find('a')['href']
                print(f"Tytuł: {title}, Link: {link}")
            except Exception as e:
                print(f"Błąd podczas pobierania danych z wyniku: {e}")
                continue

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    finally:
        # Zamknij przeglądarkę
        driver.quit()


# Przykład użycia
scrap_olx('laptop')
