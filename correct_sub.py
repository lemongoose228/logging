with open("tmp/sub.log", "r") as f:
    lines = f.readlines()

    words = ["Публикация запущена на машине:", "Подписчик получил id:",
               "Подключение к брокеру", "Началось прослушивание пользователя",
               "Получено сообщение:", "Прослушивание прекратилось"]

    dictID = {}

    for line in lines:
        userid = line.strip()[-10:-1]

        if userid not in dictID.keys():
            dictID[userid] = 0

        if words[dictID[userid]] in line.strip():
            if words[dictID[userid]] == words[-1] and words[-1] in line:
                dictID[userid] = 0
            else:
                dictID[userid] += 1
        else:
            if words[dictID[userid]] == words[-1] and words[-2] in line:
                continue
            print("Логи неправильные")
            exit()

    print("Логи правильные")