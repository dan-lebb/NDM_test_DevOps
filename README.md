# Nginx X-Forwarded-For chain test

Тестовый стенд демонстрирует корректную работу заголовка
X-Forwarded-For в цепочке reverse proxy nginx.

## Задача

Требуется:

- сохранить IP клиента
- сохранить IP всех nginx в цепочке
- защититься от подделки X-Forwarded-For клиентом

## Особенности решения

- каждый nginx добавляет свой IP в X-Forwarded-For
- недоверенные клиентские XFF уничтожаются
- trusted proxy определяются по статическим IP nginx
- используется Docker network со статическими IP

## Используемые технологии

- nginx
- docker compose
- flask

---

# Запуск

## Запуск стенда

```bash
docker compose up --build
```

---

# Проверка

## 1. Запрос через nginx1

```bash
curl localhost:8081
```

Ожидаемый маршрут:

```text
client -> nginx1 -> nginx2 -> nginx3 -> app
```

Пример результата:

```text
X-Forwarded-For:
CLIENT_IP,
172.30.0.11,
172.30.0.12
```

---

## 2. Запрос через nginx2

```bash
curl localhost:8082
```

Ожидаемый маршрут:

```text
client -> nginx2 -> nginx3 -> app
```

---

## 3. Запрос через nginx3

```bash
curl localhost:8083
```

Ожидаемый маршрут:

```text
client -> nginx3 -> app
```

---

## 4. Проверка защиты от spoofing

```bash
curl \
-H "X-Forwarded-For: 8.8.8.8" \
localhost:8081
```

Ожидаемый результат:

- IP 8.8.8.8 отсутствует
- nginx формирует корректный XFF самостоятельно

Пример:

```text
X-Forwarded-For:
172.30.0.1,
172.30.0.11,
172.30.0.12
```

---

# Как работает защита

Если запрос приходит:

- НЕ от trusted proxy
  nginx уничтожает клиентский X-Forwarded-For
  и создает новый

- ОТ trusted proxy
  nginx продолжает цепочку X-Forwarded-For

---

# Trusted proxy

Trusted proxy:

- nginx1 → 172.30.0.11
- nginx2 → 172.30.0.12
- nginx3 → 172.30.0.13
