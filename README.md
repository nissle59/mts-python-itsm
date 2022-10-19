# ITSM CLASS

itsm.py

Класс способен разбирать типичное письмо от ITSM (как задачи, так и инциденты) и возвращать JSON в ответе функции, либо
в файле.

содержит следующие методы:

```python
def load_task(
        input_lines)  # вводные строки (в формате списка)


def load_inc(
        input_lines)  # вводные строки (в формате списка)


# Следующие функции требуют предварительного вызова одной из функций выше

def to_json()  # возвращает форматированную JSON строку


def to_json_file(
        f)  # имя файла для записи форматированной JSON строки
```

### Примеры выдачи:

> #### Формат примера JSON для типичной задачи:

```yaml
{
  "type": "task",
  "root": {
    "task-sla": "<TASK-SLA>",
    "itsm-smart": "<TASK-SMART-ITSM-LINK>",
    "itsm-remedy": "<TASK-REMEDY-LINK>",
    "initiator": "<TASK-INITIATOR-FULLNAME>",
    "login": "<TASK-INITIATOR-LOGIN>",
    "department": "<TASK-INITIATOR-DEPARTMENT>",
    "job-position": "<TASK-INITIATOR-JOB-POSITION>",
    "email": "<TASK-INITIATOR-EMAIL>",
    "request-type": "<TASK-TYPE>",
    "task-header": "<TASK-HEADER>",
    "request-number": "<TASK-REQUREST-NUMBER",
    "task-number": "<TASK-NUMBER>",
    "creation-date": "<TASK-CREATION-DATE>",
    "system": "<TASK-SYSTEM>",
    "role": "<TASK-SYSTEM-ROLE>",
    "access-type": "<TASK-ACCESS-TYPE>",
    "description": "<TASK-DESCRIPTION>",
    "network-segment": "<TASK-SYSTEM-NETWORK-SEGMENT>",
    "comment": "<TASK-COMMENT>",
    "getters": [
      {
        "family-name": "<GETTER-FAMILY-NAME>",
        "first-name": "<GETTER-FIRST-NAME>",
        "last-name": "<GETTER-LAST-NAME>",
        "login": "<GETTER-LOGIN>",
        "department": "<GETTER-DEPARTMENT>",
        "job-position": "<GETTER-JOB-POSITION>",
        "email": "<GETTER-EMAIL>"
      },
      {
        "family-name": "<GETTER-FAMILY-NAME>",
        "first-name": "<GETTER-FIRST-NAME>",
        "last-name": "<GETTER-LAST-NAME>",
        "login": "<GETTER-LOGIN>",
        "department": "<GETTER-DEPARTMENT>",
        "job-position": "<GETTER-JOB-POSITION>",
        "email": "<GETTER-EMAIL>"
      }
    ]
  }
}
```

> #### Формат JSON для типичного инцидента:

```yaml
{
  "type": "inc",
  "root": {
    "affection": "<INC-AFFECTION>",
    "urgency": "<INC-URGENCY>",
    "priority": "<INC-PRIORITY>",
    "planned-datetime-sla": "<INC-SLA>",
    "inc-number": "<INC-NUMBER>",
    "initiator": "<INITIATOR-NAME>",
    "short-desc": "<INCIDENT-SHORT-DESCRIPTION>",
    "description": "<INCIDENT-FULL-DESCRIPTION>",
    "equipment": {
      "hostname": "<EQUIPMENT-HOSTNAME>",
      "type": "<EQUIPMENT-TYPE>",
      "ip": "<EQUIPMENT-IP>",
      "model": "<EQUIPMENT-MODEL>",
      "sn": "<EQUIPMENT-SERIAL-NUMBER>",
      "macroregion": "<EQUIPMENT-MACROREGION>",
      "ims-link": "<EQUIPMENT-IMS-LINK>",
      "check-date": "<EQUIPMENT-LAST-CHECK-DATE>"
    },
    "category": "<INC-CATEGORY>"
  }
}
```
