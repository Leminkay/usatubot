import requests
from bs4 import BeautifulSoup
import psycopg2

url = 'https://ugatu.su/abitur/ratelist/bachelor/'

### may remove later, dunno if i need this
unit = {'Головной ВУЗ': 1, 'Филиал ФГБОУ ВО "УГАТУ" в г. Ишимбае': 2, 'Филиал ФГБОУ ВО "УГАТУ" в г. Кумертау': 3}
edform = {'Очная': 1, 'Заочная': 2, 'Очно-заочная': 3}
EducationLevel = {'Бакалавриат': 'B', 'Специалитет': 'S'}
specValue = {"168": "01.03.02 Прикладная математика и информатика",
             "169": "01.03.04 Прикладная математика",
             "170": "02.03.01 Математика и компьютерные науки",
             "171": "02.03.03 Математическое обеспечение и администрирование информационных систем",
             "172": "09.03.01 Информатика и вычислительная техника",
             "173": "09.03.02 Информационные системы и технологии",
             "174": "09.03.03 Прикладная информатика",
             "175": "09.03.04 Программная инженерия",
             "177": "10.03.01 Информационная безопасность",
             "179": "11.03.02 Инфокоммуникационные технологии и системы связи",
             "180": "11.03.04 Электроника и наноэлектроника",
             "182": "12.03.01 Приборостроение",
             "183": "12.03.04 Биотехнические системы и технологии",
             "184": "13.03.01 Теплоэнергетика и теплотехника",
             "185": "13.03.02 Электроэнергетика и электротехника",
             "186": "13.03.03 Энергетическое машиностроение",
             "188": "15.03.01 Машиностроение",
             "189": "15.03.02 Технологические машины и оборудование",
             "190": "15.03.04 Автоматизация технологических процессов и производств",
             "191": "15.03.05 Конструкторско-технологическое обеспечение машиностроительных производств",
             "192": "15.03.06 Мехатроника и робототехника",
             "194": "20.03.01 Техносферная безопасность",
             "196": "22.03.01 Материаловедение и технологии материалов",
             "197": "23.03.01 Технология транспортных процессов",
             "198": "24.03.04 Авиастроение",
             "199": "24.03.05 Двигатели летательных аппаратов",
             "202": "25.03.01 Техническая эксплуатация летательных аппаратов и двигателей",
             "314": "25.03.01 Техническая эксплуатация летательных аппаратов и двигателей (Иностранцы)",
             "203": "27.03.01 Стандартизация и метрология",
             "204": "27.03.02 Управление качеством",
             "205": "27.03.03 Системный анализ и управление",
             "206": "27.03.04 Управление в технических системах",
             "207": "27.03.05 Инноватика",
             "209": "28.03.02 Наноинженерия",
             "210": "38.03.01 Экономика",
             "211": "38.03.02 Менеджмент",
             "212": "38.03.03 Управление персоналом",
             "213": "38.03.04 Государственное и муниципальное управление",
             "214": "38.03.05 Бизнес-информатика",
             "176": "09.05.01 Применение и эксплуатация автоматизированных систем специального назначения",
             "178": "10.05.05 Безопасность информационных технологий в правоохранительной сфере",
             "181": "11.05.04 Инфокоммуникационные технологии и системы специальной связи",
             "187": "13.05.02 Специальные электромеханические системы",
             "193": "15.05.01 Проектирование технологических машин и комплексов",
             "195": "20.05.01 Пожарная безопасность",
             "200": "24.05.02 Проектирование авиационных и ракетных двигателей",
             "201": "24.05.06 Системы управления летательными аппаратами",
             "208": "27.05.01 Специальные организационно-технические системы",
             "215": "38.05.01 Экономическая безопасность",
             "276": "09.03.03 Прикладная информатика (Ишимбай)",
             "277": "13.03.02 Электроэнергетика и электротехника",
             "278": "15.03.04 Автоматизация технологических процессов и производств",
             "273": "09.03.03 Прикладная информатика (Кумертау)",
             "274": "15.03.04 Автоматизация технологических процессов и производств",
             "275": "24.05.06 Системы управления летательными аппаратами"
             }
doc = ['Конкурсная ситуация', 'Список поступающих']
docOsn = ['Бюджет', 'Контракт']
comment = ["Все", 'общий конкурс', 'без вступительных', 'особое право', 'целевая квота']


###


# parsing page to get users
def get_users(text):
    soup = BeautifulSoup(text, "html.parser")
    data = []
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        # cols = [col.text.strip() for col in cols]

        for i in range(len(cols)):
            cols[i] = cols[i].text.strip()

            if cols[i] == "-":
                cols[i] = 0
            if str(cols[i])[:3] == "Нет" and i > 6 :
                cols[i] = "false"
            if str(cols[i])[:2] == "Да" and i > 6:
                cols[i] = "true"
            #print(cols[i])
        if cols[10] == 'Без вступительных':
            cols[2] = 1337
            cols[8] = 'true'
        data.append(cols)
    print(data[1:])
    return data[1:]


# get page text
def request_page(curSession, specVal, token):
    # the only thing that matters in payload is specValue, even if Education Level or unit is not matching
    payload = {'csrfmiddlewaretoken': token, 'unit': 1, 'edform': edform['Очная'],
               'EducationLevel': EducationLevel['Бакалавриат'], 'specValue': specVal, 'doc': doc[0],
               'docOsn': docOsn[0],
               'comment': comment[0]}

    r = curSession.post(url, data=payload)
    return r.text


# get token through get request
def set_csrftoken(curSession):
    r = curSession.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find_all('input', type='hidden')[0]['value']
    return token


s = requests.Session()
s.headers['Content-Type'] = 'application/x-www-form-urlencoded'
s.headers['Referer'] = url

# example
csrftoken = set_csrftoken(s)
page_text = request_page(s, 203, csrftoken)
usrs = get_users(page_text)
#print(usrs)


def insert_row(abitur, conn, spec, cTime):
    cur = conn.cursor()
    # informatics = physics :)

    cur.execute(
        "INSERT INTO USATU (name,sum,math,inf,rus,inv, agreed, advantage, original, spec, upd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (abitur[1], abitur[2], abitur[3], abitur[4], abitur[5], abitur[6], abitur[7], abitur[8], abitur[9], spec, cTime)
    )
    conn.commit()


def insert_all(curSession, conn, cTime):
    csrftoken = set_csrftoken(curSession)
    for key in specValue:
        page_data = request_page(curSession, key, csrftoken)
        print(specValue[key])
        usrs = get_users(page_data)
        for usr in usrs:
            insert_row(usr, conn, key, cTime)


conn = psycopg2.connect(dbname='Bank', user='postgres', password='12345', host='localhost')

cur = conn.cursor()

insert_all(s, conn, 12313)


conn.close()
