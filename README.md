🔶 SECUNDA -> Organizations calendar
---
---

## 🔹 Примечания:

```
Для доступа к API используется ключ, доступные ключи:
TEST_KEY_1 и TEST_KEY_2
Без них API будет отдавать Access Denied
(Ключи автоматически добавлены в поле в Swagger)
```

## 🔹 Старт через Docker (Рекомендуется):

#### **Остановить postgres-сервис во избежание проблем с портами в контейнере:**

```bash
task stop_postgres_service
```

#### **Создать сеть для контейнеров:**

```bash
task create_docker_network
```

#### **Собрать сборку:**

```bash
task build_docker
```

### Открыть адрес документации FastAPI (Для удобства) -> http://0.0.0.0:8000/docs , Тестировать функционал

> **Доп команды:**

**Проверить контейнеры**

```bash
task check_containers
```

**Запустить основной сервис, если базово не включился**

```bash
task run_service
```

**Остановить контейнеры:**

```bash
task stop_service
```

**Удалить контейнеры: (Внимание: Удаляет также образ postgres:16.3-alpine3.19)**

```bash
task delete_containers
```

**Удалить сеть для контейнеров:**

```bash
task delete_docker_network
```

**Включить postgres-сервисы**

```bash
task start_postgres_service

```

---

## 🔹 Локальный старт:

#### **Установить зависимости (Не забывая про .venv)**:

```bash
pip install -r requirements.txt
```

#### **Остановить postgres-сервис во избежание проблем с портами в контейнере:**

```bash
task stop_postgres_service
```

#### **Локально поднять postgres в докере с нужными credentials**

```bash
task start_postgres_in_docker
```

#### **'Накатить' базовую миграцию:**

```bash
alembic upgrade head
```

#### **Запустить сервер:**:

```bash
python src/core/root/main.py
```

### Открыть адрес документации FastAPI (Для удобства) -> http://0.0.0.0:8000/docs , Тестировать функционал

## 🔹 Дополнительные инструменты:

#### **Линтер:**:

```bash
flake8 ./
```

#### **Типизатор:**

```bash
mypy ./
```
