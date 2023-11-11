from bs4 import BeautifulSoup
from selenium import webdriver
import logging


class FeedbackParserOZN:
    def __init__(self, url):
        self.url = url
        self.html_content = None  # Добавим переменную для хранения HTML-кода

    def get_html(self):
        if self.html_content is not None:
            return self.html_content

        url = self.url
        if not url:
            return "Не удалось получить ссылку на товар. Попробуйте еще раз."
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        final_url = driver.current_url
        driver.quit()
        transformed_url = f'{final_url.split("?")[0]}reviews'
        logging.info(f"Получение HTML content из URL: {transformed_url}")
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get(transformed_url)
        self.html_content = driver.page_source  # Сохраняем HTML-контент
        driver.quit()
        return self.html_content


    def get_reviews_from_html(self):
        html_content = self.get_html()
        if not html_content:
            return "Не удалось получить html. Попробуйте еще раз."
        soup = BeautifulSoup(html_content, 'html.parser')
        logging.info("Получение отзывов из HTML")
        reviews = soup.find_all('div', class_='up3 p1v')
        all_reviews = []
        for review in reviews:
            p4us = review.find_all('div', class_='p4u')
            for p4u in p4us:
                pu4 = p4u.find('div', class_='pu4')
                if pu4:
                    pu4_text = pu4.get_text(strip=True)
                    u3p = p4u.find('span', class_='u3p').get_text(strip=True)
                    all_reviews.append(f"{pu4_text}: {u3p}")
                else:
                    u3p = p4u.find('span', class_='u3p').get_text(strip=True)
                    all_reviews.append(f"Комментарий: {u3p}")
        return all_reviews


    def get_item_name(self):
        html_content = self.get_html()
        if not html_content:
            return "Не удалось получить html. Попробуйте еще раз."

        logging.info("Извлечение наименования товара из HTML")
        soup = BeautifulSoup(html_content, 'html.parser')
        m6l_div = soup.find('div', class_='m6l')

        if m6l_div:
            name = m6l_div.get_text(strip=True).split(',')[0]
            # Обрезаем наименование до 25 символов
            truncated_name = name[:30]
            return truncated_name
        else:
            return "Не удалось получить наименование товара. Попробуйте еще раз."

    def get_formatted_reviews(self):
        reviews_text = self.get_reviews_from_html()
        name = self.get_item_name()
        if not reviews_text or not name:
            return "Не удалось получить отредактированные отзывы. Попробуйте еще раз."
        logging.info("Редактирование отзывов")
        formatted_text = "Напиши основные плюсы и минусы товара {} исходя из отзывов:".format(name)
        for review in reviews_text:
            if len(formatted_text) + len(review) <= 4000:
                formatted_text += "\n" + review
            else:
                break
        return formatted_text