Основная программа в файле: main_ver1.py
Запускается через zapusk_main_ver1.py или напрямую main_ver1.py
Файл Start_message.xlsx стартовые посты на 29.01.2023 г.

Парсинг телеграмм каналов @Bigpowernews (BigpowerNews)
@blackenergydung (ЧОрний Енерготрейдер)
@chief_energy (Главный энергетик)
@dsm_so (DSM SO)
@electricalnet (Электрические Сети в Системе)
@energo_blog (Energo.blog)
@energo3 (ЭнергоТройка)
@energoatlas (ЭнергоА++)
@Law_Energy (LawEnergy)
@lawelectric (Энергоюристы)
@manevichsquare (КВАДРАТ МАНЕВИЧА)
@missia261 (Миссия261)
@npace (Сообщество потребителей энергии)
@npsr_real (ЭнергоPROсвет)
@pere_tok (Переток для своих)
@riseofelectro (Высокое напряжение)
@shadow_minenergorf (Теневое Минэнерго)
@SovetBezRynka (СоветБезРынка)
@starshijpodomu (Старший по дому (ЖКХ))
@taxelectric (Налоги в электроэнергетике)
@teplovichok (Teplovichok)
@zhane_ru (Правовые аспекты энергоснабжения)
@zlobunal (Zлобунальщик)
@polina_green (Полина Смертина Ъ) с 28.01.2023 NEW!

парсинг по ключевым словам: ('пени\w|штраф\w|потреб\w|перм\w|рсв|рын\w|цен\w|совет\w|резер\w|квт|ЭЭ|мощность|рээ|орэ|дпм|тариф\w|фас|безучет\w|потребл\w|суд\w|потребит\w|поставка\w|качеств\w|гп\w|уровен\w|уровн\wнапряжен\w|учёт\wпоказан\w|учет\w|мкд\w|тепл\w|ипу|одпу|закон\w|оспор\w|акт\w|бездоговор\w|счет\w|счёт\w|прогн\w|квитанц\w|оплат\w|руб|мвт|управлен\wспрос\w|прав\w|объе\w|объё\w')
send to https://t.me/ProElEnPK

Инструкция "под себя"
создайте бота, получите токен и запишите его в переменную token (token = a[0].split(' = ')[1].replace('"', '').replace('\n', ''))
получите channel_id куда хотите публиковать посты, запишите в переменную channel_id (channel_id = a[1].split(' = ')[1].replace('"', '').replace('\n', ''))
откройте файл "Start_message.xlsx" и поменяйте в столбце "chan" имена каналов (откуда брать), в столбце "start_message" укажите номер поста, с которого парсить
файл "Start_message.xlsx" сохраните
в коде в переменной pattern укажите ключевые слова
каналы, которые не отображают контент по ссылке в web интерфейсе, например, https://t.me/ProSbyt/507, https://t.me/s/ProSbyt/507 не парсятся
