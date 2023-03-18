"""
created by AuF22
https://github.com/AuF22
"""
import requests
from config import pin as PIN
from datetime import datetime


header = {
    "X-Road-Client": "central-server/COM/60000061/ELETCAPITAL"
}


def respone_addres(PIN) -> dict:
    """Функция отправляющая запрос по ПИНу для фактического адреса проживания"""
    url = "http://31.186.50.227/r1/central-server/GOV/70000050/sanaripaymak-service/address-fact/{pin}"

    print(url.format(pin=PIN))
    r = requests.get(url.format(pin=PIN), headers=header)
    print(r)

    # проверяем статус 204 значит, неправильный пин
    if r.status_code != 200:
        if r.status_code != 204:
            return False
        return 'Вы указали неверный PIN'
    else:
        return r.json()


def respon_family(PIN) -> dict:
    """Функция отправляющая запрос по ПИНу для членов семьи"""
    url = "http://31.186.50.227/r1/central-server/GOV/70000050/sanaripaymak-service/family-members/{pin}"
    r = requests.get(url.format(pin=PIN), headers=header)
    data = r.json()
    
    #проверяем статус 405 значит, у клиента нет семьи
    if data.get("code") == 405:
        return {}
    return data


def main():
    PIN = input("Введите ПИН:")
    addres = respone_addres(PIN=PIN)
    data = {**addres}
    
    if addres:
        if len(addres) == 0:
            print("Вы ввели неверный ПИН")
        else:
            family = respon_family(PIN=PIN)

            if family.get('members') is None:
                pass
            else:
                members = family.get("members")
                for member in members:
                    data = {**data, **member}
    
        with open(f"response\{data.get('pin')}.txt", encoding="utf-8", mode='w') as file:
            file.write(f"Время запроса: {datetime.now().strftime('%H:%M:%S, %d.%m.%Y')} г.\n")
            for key, value in data.items():
                file.write(f"{key}:{value}\n")


    else:
        print('Ошибки на сервере')


if __name__ == "__main__":
    main()
