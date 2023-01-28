import requests #  Делать запросы к сайту
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

with open('token.txt') as f: #token.txt файл с token, channel_id
    a = [line for line in f.readlines()]
token = a[0].split(' = ')[1].replace('"', '').replace('\n', '') #token from send, exemple, bot_telegram
channel_id = a[1].split(' = ')[1].replace('"', '').replace('\n', '') #channel_id to send

def send_telegram(text, token, channel_id):
    # функция отправки сообщения в целевой канал
    token =   token
    url = "https://api.telegram.org/bot"
    channel_id = channel_id
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })
    print(r.status_code, r.reason, r.content)
    if r.status_code != 200:
        raise Exception("post_text error")

# Список каналов и nomer_start
xls = pd.ExcelFile(r'Start_message.xlsx') # Файл таблица
df = xls.parse("Start_message") # Лист таблица
df = df.groupby('chan')[['start_message']].max().sort_index(key=lambda x: x.str.lower()).reset_index().reset_index() # Выбор поста с максимальным номером
chan_lst = df['chan'].to_list() # Список каналов
start_message_lst = df['start_message'].to_list() #Список nomer_start
dictionary = dict(zip(chan_lst, start_message_lst)) # Словарь key = каналы и value = nomer_start
dictionary_old = dictionary.copy()
print(dictionary)
chan_to_df = [] # имя для записи итогов
nomer_finish_post_to_df = [] # номера последних для записи итогов

#Парсинг
for key_chan, val_start_message in dictionary.items():
    chan = key_chan # канал
    chan_url = 'https://t.me/' + chan # ссылка на канал
    chan_prew_url = 'https://t.me/s/' + chan # ссылка на превью (последние записи в канале)

    res = requests.get(chan_prew_url) # запрос к ссылка на превью
    soup = BeautifulSoup(res.text, 'html.parser') # запись в переменную ответа для парсинга

    # поиск даты последнего поста
    title_time_date_lst = [] # список дат
    title_time = soup.find_all("time", 'class'=='time') # поиск по тегу "time", 'class'=='time'
    for date in title_time:
        title_time_date_lst.append(date.get('datetime')) # создание списка дат

    try:
        ind_date_finish = title_time_date_lst[-1] # дата последнего поста
        ind_id_date_finish = title_time_date_lst.index(ind_date_finish)  # индекс даты последнего поста в title_time_date_lst
        print(f'дата последнего поста: {ind_date_finish}, канал: {chan}')
    except IndexError:
        continue

    #поиск номера последнего поста
    title_message = soup.find_all("a", 'class'=='tgme_widget_message_date') # поиск тега a и class = tgme_widget_message_date

    for i in range(len(title_message)):
        if title_message[i].find_all("time", 'class'=='time') == []:
            continue
        i += 1 #счетчик индекса

    ind_title_message = i - 1  # индеск последнего поста
    try:
        nomer_finish_post = title_message[ind_title_message].get('href').split('/')[4]  #номер последнего поста
        print(f'номер последнего поста: {nomer_finish_post}, канал: {chan}')
        print(f'номер стартого поста: {val_start_message}, канал: {chan}')
        chan_to_df.append(chan) # список каналов для итогов
        nomer_finish_post_to_df.append(nomer_finish_post) # список постов для итогов
    except IndexError:
        continue

    nomer_start = val_start_message #номер нулевого поста для канала chan

    #pattern. ключевые слова
    pattern = re.compile('пени\w|штраф\w|потреб\w|перм\w|рсв|рын\w|цен\w|совет\w|резер\w|квт|ЭЭ|мощность|рээ|орэ|дпм|тариф\w|фас|безучет\w|потребл\w|суд\w|потребит\w|поставка\w|качеств\w|гп\w|уровен\w|уровн\wнапряжен\w|учёт\wпоказан\w|учет\w|мкд\w|тепл\w|ипу|одпу|закон\w|оспор\w|акт\w|бездоговор\w|счет\w|счёт\w|прогн\w|квитанц\w|оплат\w|руб|мвт|управлен\wспрос\w|прав\w|объе\w|объё\w')
    lststr = [] #лист статей для проверки
    lststr_to_print = []  #лист статей для публикации

    #парсинг канала
    i_post = nomer_start #номер поста, с которого начать парсинг канала
    while int(i_post) < int(nomer_finish_post): # int(4119+3): - test и int(nomer_finish_post):
        try:
            url = chan_url + "/" + str(i_post)
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find("meta", attrs={'property': 'og:description'})
            title_time = soup.find_all("time", 'class' == 'time')
            if len(pattern.findall(title["content"])) > 0:
                lststr_to_print.append(f'источник: @{url.split("/").pop(-2)}, ссылка: {url}: {title["content"]}')
            i_post += 1
            time.sleep(3)
        except IndexError:
            continue

    time.sleep(15)
    #отправка сообщения
    try:
        for el_lststr_to_print in lststr_to_print:
            time.sleep(3)
            if len(el_lststr_to_print) > 4096:
                send_telegram(el_lststr_to_print[:(4096-len(' ....далее в источнике'))] + ' ....далее в источнике', token, channel_id)
            else:
                send_telegram(el_lststr_to_print, token, channel_id)
            #print(f'номер сообщения: {lststr_to_print.index(el_lststr_to_print)+1}, сообщение: {el_lststr_to_print}')
            #send_telegram(el_lststr_to_print)
    except IndexError:
        continue

# Запись итогов
data = {'chan': chan_to_df, 'start_message': nomer_finish_post_to_df}
df_finish = pd.DataFrame.from_dict(data)
df_finish["start_message"] = pd.to_numeric(df_finish["start_message"])

pd.concat([df,df_finish]).to_excel('Start_message.xlsx', sheet_name='Start_message', index=False)

# Вывод словаря сколько было и сколько стало
xls = pd.ExcelFile(r'Start_message.xlsx') # Файл таблица
df = xls.parse("Start_message") # Лист таблица
df = df.groupby('chan')[['start_message']].max().sort_index(key=lambda x: x.str.lower()).reset_index().reset_index() # Выбор поста с максимальным номером
chan_lst = df['chan'].to_list() # Список каналов
start_message_lst = df['start_message'].to_list() #Список nomer_start
dictionary = dict(zip(chan_lst, start_message_lst)) # Словарь key = каналы и value = nomer_start

print("стартовые номера постов:")
print(dictionary_old)
print("новые номера постов:")
print(dictionary)
