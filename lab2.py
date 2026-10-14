state = "IDLE"
last_action = "IDLE"

charge_streak = 0

data = 0
charge = 10
fuel = 10

scanned_here = 0
data_total = 0

states = [
    "IDLE",
    "I",
    "SCAN",
    "S",
    "TRANSMIT",
    "T",
    "CHARGE",
    "C",
    "MANEUVER",
    "M",
    "QUIT",
    "Q",
]

print("Связь со спутником установлена.")
print("Команды: IDLE/I, SCAN/S, TRANSMIT/T, " "CHARGE/C, MANEUVER/M, QUIT/Q")

while state != "QUIT":
    print(f"data = {data}, charge = {charge}, fuel = {fuel}")
    state = input("Ожидание команды: ").strip().upper()
    if state not in states:
        print("Ошибка интерпретатора.")
        charge -= 1
        state = "IDLE"
    elif state == "QUIT" or state == "Q":
        print(f"Всего передано данных: {data_total}")
        print("Завершение работы...")
        state = "QUIT"
    elif state == "IDLE" or state == "I":
        state = "IDLE"
    elif state == "CHARGE" or state == "C":
        if charge_streak < 2:
            charge += 3
            charge_streak += 1
            if charge > 10:
                charge = 10
                fuel -= 1
                print("Избыток заряда. Потрачено 1 топливо на охлаждение.")
            print("Зарядка завершена.")
            last_action = "CHARGE"
        else:
            print("Ошибка. Двойная зарядка невозможна.")
            charge -= 1
        state = "IDLE"
    elif state == "SCAN" or state == "S":
        charge_streak = 0
        if charge < 1:
            print("Ошибка. Нехватка энергии.")
            charge -= 1
        elif data >= 10:
            print("Память заполнена. Передайте данные на станцию.")
            charge -= 1
        elif scanned_here >= 5:
            print("Лимит сканирования на этой точке исчерпан.")
            charge -= 1
        else:
            charge -= 1
            if charge >= 2:
                charge -= 2
                if last_action == "MANEUVER":
                    scanned = 2
                else:
                    scanned = 5
                scanned = min(scanned, 5 - scanned_here, 10 - data)
                data += scanned
                scanned_here += scanned
                print(f"Сканирование завершено. Получено {scanned} данных.")
                last_action = "SCAN"
            else:
                print("Ошибка. Недостаточно заряда для сканирования.")
                charge -= 1
        state = "IDLE"
    elif state == "TRANSMIT" or state == "T":
        charge_streak = 0
        if last_action == "MANEUVER":
            print("Ошибка. Передача сразу после перемещения невозможна.")
            charge -= 1
        elif data == 0:
            print("Ошибка. Данные не найдены.")
            charge -= 1
        elif charge < 1:
            print("Ошибка. Нехватка энергии.")
            charge -= 1
        else:
            charge -= 1
            if charge >= 4:
                charge -= 4
                data_total += data
                data = 0
                print("Передача данных успешно завершена.")
                print(f"Всего передано данных: {data_total}")
                last_action = "TRANSMIT"
            else:
                print("Ошибка. Недостаточно заряда для передачи.")
                charge -= 1
        state = "IDLE"
    elif state == "MANEUVER" or state == "M":
        charge_streak = 0
        if last_action == "CHARGE":
            print("Ошибка. Перемещение сразу после зарядки невозможно.")
            charge -= 1
        elif fuel < 1:
            print("Ошибка. Недостаточно топлива.")
            charge -= 1
        elif charge < 1:
            print("Ошибка. Нехватка энергии для перехода.")
            charge -= 1
        else:
            charge -= 1
            fuel -= 1
            scanned_here = 0
            print("Перемещение завершено.")
            last_action = "MANEUVER"
        state = "IDLE"
    if charge <= 0 or fuel <= 0:
        print(f"Всего передано данных: {data_total}")
        print("Связь со спутником потеряна.")
        state = "QUIT"
