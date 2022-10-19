import json


# Парсер писем от ITSM (любой набор данных, главное - соответствие шаблону "ОПИСАНИЕ - ПОЛУЧАТЕЛИ - РЕШЕНИЕ")

class Itsm:
    __info = {}
    full_response = {}

    translate_dict = {
        '"Инициатор":': '"initiator":',
        "Логин": "login",
        "Подразделение": "department",
        "Должность": "job-position",
        "Email": "email",
        "Тип запроса": "request-type",
        "Заголовок задачи": "task-header",
        "Номер запроса": "request-number",
        "Номер задачи": "task-number",
        "Дата создания запроса": "creation-date",
        "Система": "system",
        "Роль": "role",
        "Тип доступа": "access-type",
        "Описание": "description",
        "Сегмент сети": "network-segment",
        "Комментарий": "comment",
        "Фамилия": "family-name",
        '"Имя":': '"first-name":',
        "Отчество": "last-name",
        "Открыть Smart ITSM (Работает только в Chrome)": "itsm-smart",
        "Открыть Remedy ITSM": "itsm-remedy",
        "Срок выполнения задачи": "task-sla",
        "Раздел": "template-block",
        "Название шаблона": "template-name",
        "Местоположение системы": "system-location",
        "Информационная система": "system",
        "Подтверждаю, что доступ предоставлен ранее.": "access-approved",
        "Обоснование": "comment",
        '"Влияние":': '"affection":',
        '"Срочность":': '"urgency":',
        '"Приоритет":': '"priority":',
        '"Планируемая дата решения (МСК)":': '"planned-datetime-sla":',
        '"Имя хоста":': '"hostname":',
        '"Тип":': '"type":',
        '"IP-адрес":': '"ip":',
        '"Модель":': '"model":',
        '"Серийный номер":': '"sn":',
        '"Макрорегион":': '"macroregion":',
        '"Ссылка на описание оборудования":': '"ims-link":',
        '"Дата проверки":': '"check-date":',
        '"Категория":': '"category":'
    }

    def __init__(self):
        pass

    def load_task(self, input_lines):
        desc_idx = 0
        getters_idx = 0
        previous_idx = 0
        endline_idx = 0

        for line in input_lines:
            if line.find('--- ОПИСАНИЕ') > 0:
                desc_idx = input_lines.index(line)
            if line.find('--- ПОЛУЧАТЕЛИ') > 0:
                getters_idx = input_lines.index(line)
            if line.find('--- РЕШЕНИЕ') > 0:
                previous_idx = input_lines.index(line)
            if line.find('RequestDisplay.aspx') > 0:
                endline_idx = input_lines.index(line) - 2

        start_lines = input_lines[0:desc_idx]
        desc_lines = input_lines[desc_idx + 1:getters_idx]
        getters_lines = input_lines[getters_idx + 1:previous_idx]
        previous_lines = input_lines[previous_idx + 1:endline_idx]

        # -------- Первые строки письма ----------
        for line in start_lines:
            if line != '':
                if line[0] == '[':
                    ss = line.replace('>[', ';').replace(']<', '|').replace('[', '').replace(']', '').replace('>',
                                                                                                              '').split(
                        ';')
                    for s in ss:
                        key = s.split('|')[0]
                        value = s.split('|')[1]
                        self.__info.update({key.strip(): value.strip()})
                elif line.find('Срок выполнения задачи:') > -1:
                    buf = line.split(':')
                    key = buf[0]
                    del buf[0]
                    value = ':'.join(buf)
                    self.__info.update({key.strip(): value.strip()})

        # ----------- ОПИСАНИЕ ЗАДАЧИ -------------
        for line in desc_lines:
            if line.find(':') > 0:
                if (line[0] != '[') and (line[0] != 'h'):
                    buf = line.split(':')
                    key = buf[0]
                    del buf[0]
                    value = ':'.join(buf)
                    if value.find('<') > 0:
                        v = value.split(';')
                        # print(v)
                        self.__info.update({key.strip(): v[0].strip()})
                        self.__info.update({'Email': v[1].strip().split('<')[0].strip()})
                    else:
                        self.__info.update({key.strip(): value.strip()})

        self.__info.pop('Получатель сервиса')
        self.__info.pop('Руководитель получателя')

        # ---------- ПОЛУЧАТЕЛИ СЕРВИСА -----------
        getters_array = []
        getters_dict = {}
        while len(getters_lines) > 0:
            if (getters_lines[0].find(':') < 0) and (getters_lines[0] != ''):
                buf = getters_lines[0].split()
                getters_dict.update({'Фамилия': buf[0].strip()})
                getters_dict.update({'Имя': buf[1].strip()})
                getters_dict.update({'Отчество': buf[2].strip()})
                del getters_lines[0]
            elif getters_lines[0].find(':') > 0:
                buf = getters_lines[0].split(':')
                key = buf[0]
                del buf[0]
                value = ':'.join(buf)
                if value.find(';') > 0:
                    v = value.split(';')
                    getters_dict.update({key.strip(): v[0].strip()})
                    getters_dict.update({'Email': v[1].strip()})
                else:
                    getters_dict.update({key.strip(): value.strip()})
                del getters_lines[0]
            else:
                getters_array.append(getters_dict)
                getters_dict = {}
                del getters_lines[0]

        self.__info.update({'getters': getters_array})

        # ---------- РЕШЕНИЕ ПРЕДЫДУЩИХ ЗАДАЧ -----------
        del previous_lines[0]
        task_dicts = []
        while len(previous_lines) > 0:
            if previous_lines[0].find('->') > 0:
                prev_arr = previous_lines[0].replace(')', ');').replace(' #', ' - #').replace('-->', '-->;').replace(
                    ' ФИО', ';ФИО').replace(' командой', ';команда').split(';')
                del prev_arr[0]
                for i in prev_arr:
                    if i == '':
                        del prev_arr[prev_arr.index(i)]
                task_arr = prev_arr[0]
                comm_arr = prev_arr[1].split(': ')
                fio_arr = prev_arr[2].split(': ')
                task_arr = task_arr.split(' - ')
                task_arr[2] = task_arr[2] + ')'
                task_arr[3] = task_arr[3][:-1]
                task_sol = previous_lines[2].strip()
                task_dict = {
                    task_arr[1]: {'status': task_arr[2], 'date': task_arr[3], 'team': comm_arr[1], 'user': fio_arr[1],
                                  'solution': task_sol}}
                task_dicts.append(task_dict)
            del previous_lines[0]
        if len(task_dicts) > 0:
            self.__info.update({'solved': task_dicts})
        self.full_response = {'type': 'task', 'root': self.__info}

    def load_inc(self, input_lines):
        self.__info = {}

        desc_line = '------------ Описание ------------'
        category_line = '------------ Категория ------------'
        endline_line = '------------------------------------------'

        desc_idx = input_lines.index(desc_line)
        category_idx = input_lines.index(category_line)
        endline_idx = input_lines.index(endline_line)

        start_lines = input_lines[0:desc_idx]
        desc_lines = input_lines[desc_idx + 1:category_idx]
        category_lines = input_lines[category_idx + 1:endline_idx]

        # ----------- START LINES INC ----------------
        buffer = start_lines[0].split(';')
        for line in buffer:
            buf = line.split(':')
            key = buf[0].strip()
            del buf[0]
            value = ':'.join(buf).strip()
            self.__info.update({key: value})
        buffer = start_lines[5]
        idx = buffer.find('INC')
        buffer = buffer[idx:]
        print(buffer)
        self.__info.update({'inc-number': buffer})

        # ----------- DESC LINES INC -----------------
        long_desc_line = 'Описание:'
        long_desc_idx = desc_lines.index(long_desc_line)
        equipment_line = 'Дополнительная информация об оборудовании:'
        equipment_idx = desc_lines.index(equipment_line)

        self.__info.update({
            'Инициатор': desc_lines[0].split(':')[1].strip(),
            'short-desc': desc_lines[1].split(':')[1].strip()
        })
        self.__info.update({'description': '\n'.join(desc_lines[long_desc_idx + 1:equipment_idx])})
        equipment = {}
        eq_lines = desc_lines[equipment_idx + 1:category_idx]
        for line in eq_lines:
            if line.find(':') > 0:
                buf = line.split(':')
                key = buf[0].strip()
                del buf[0]
                value = ':'.join(buf).strip()
                if value != '':
                    equipment.update({key: value})
        self.__info.update({'equipment': equipment})
        self.__info.update({category_lines[0].split(':')[0].strip(): category_lines[0].split(':')[1].strip()})
        self.full_response = {'type': 'inc', 'root': self.__info}

    def to_json(self):
        if len(self.__info) > 0:
            res = json.dumps(self.full_response, indent=4, sort_keys=False, ensure_ascii=False)
            for i in self.translate_dict:
                res = res.replace(i, self.translate_dict[i])
            return res.encode('utf-8')
        else:
            return '{ "type" : "error", "root" : "no data" }'.encode('utf-8')

    def to_json_file(self, f):
        if len(self.full_response) > 0:
            dataFile = open(f, "wb")
            dataFile.write(self.to_json())
            dataFile.close()
        else:
            return '{ "type" : "error", "root" : "no data" }'.encode('utf-8')
