from parser_wb import FeedbackParserWB
from gpt import GPT
import requests

url = 'https://www.wildberries.ru/catalog/122656201/detail.aspx'
extractor = FeedbackParserWB(url)
text = extractor.get_formatted_feedbacks()
# print(text)
question_str = text
gpt_instance = GPT(question_str)
print(gpt_instance.ask_gpt())


# url = 'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1180979&spp=29&nm=163405593'
# response = requests.get(url)
# data = response.json()
# root = data["data"]["products"][0]["root"]
# name = data["data"]["products"][0]["name"]
# print(name)