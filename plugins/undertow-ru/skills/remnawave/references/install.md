# Установка Panel

Новая установка Remnawave Panel с нуля: подготовка сервера, `.env`, запуск контейнеров, обязательный reverse proxy и защита панели. Обновление и переход со старых версий: [upgrade.md](upgrade.md).

## Теория

Официальная документация описывает такую install-модель:

- Remnawave Panel является главным компонентом;
- для Panel и Node требуется `Docker` с `Docker Compose plugin`;
- Panel должен публиковаться через reverse proxy;
- сервисы Remnawave нельзя выставлять в интернет напрямую, только `127.0.0.1`;
- Panel и компоненты не поддерживают обслуживание на sub-path.

## Требования

| | Panel | Node |
| --- | --- | --- |
| OS | рекомендованы Ubuntu или Debian | рекомендованы Ubuntu или Debian |
| RAM | минимум 2 GB, рекомендовано 4 GB | минимум 1 GB |
| CPU | минимум 2 cores, рекомендовано 4 | минимум 1 core |
| Storage | 20 GB | — |

- Panel может работать на меньших ресурсах, но docs это не рекомендуют: часть фоновых процессов ресурсоёмкая.
- Node сама по себе лёгкая, но `Xray-core` под нагрузкой может потреблять много CPU и RAM.
- Docker с Compose plugin: способ установки описан на странице requirements в docs.rw и в документации Docker.

## Шаги установки

1. Подготовить каталог:

   ```bash
   mkdir /opt/remnawave && cd /opt/remnawave
   ```

2. Скачать официальные `docker-compose-prod.yml` и `.env.sample` из `remnawave/backend`:

   ```bash
   curl -o docker-compose.yml https://raw.githubusercontent.com/remnawave/backend/refs/heads/main/docker-compose-prod.yml
   curl -o .env https://raw.githubusercontent.com/remnawave/backend/refs/heads/main/.env.sample
   ```

3. Сгенерировать секреты `APP_SECRET`, `METRICS_PASS`, `WEBHOOK_SECRET_HEADER`:

   ```bash
   sed -i "s/^APP_SECRET=.*/APP_SECRET=$(openssl rand -hex 64)/" .env
   sed -i "s/^METRICS_PASS=.*/METRICS_PASS=$(openssl rand -hex 64)/" .env
   sed -i "s/^WEBHOOK_SECRET_HEADER=.*/WEBHOOK_SECRET_HEADER=$(openssl rand -hex 64)/" .env
   ```

4. Сменить пароль Postgres (меняется и `POSTGRES_PASSWORD`, и пароль внутри `DATABASE_URL`):

   ```bash
   pw=$(openssl rand -hex 24) && sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$pw/" .env && sed -i "s|^\(DATABASE_URL=\"postgresql://postgres:\)[^\@]*\(@.*\)|\1$pw\2|" .env
   ```

5. Обновить в `.env` как минимум:
   - `FRONT_END_DOMAIN` — домен панели, например `panel.yourdomain.com`;
   - `SUB_PUBLIC_DOMAIN` — на первом шаге домен панели плюс `/api/sub`, например `panel.yourdomain.com/api/sub`.
6. Запустить контейнеры:

   ```bash
   docker compose up -d && docker compose logs -f -t
   ```

7. Сразу после запуска поставить reverse proxy на root path домена или subdomain.

## Состав установки

- Контейнеры из `docker-compose-prod.yml`: `remnawave` (Panel), `remnawave-db` (Postgres), `remnawave-redis` (Valkey).
- Порты Panel (`3000`, `3001`) и Postgres (`6767`) привязаны к `127.0.0.1`; наружу их публикует только reverse proxy.
- Panel связана с Valkey через Unix socket (`REDIS_SOCKET=/var/run/valkey/valkey.sock` в `.env.sample`); `REDIS_HOST` и `REDIS_PORT` — альтернатива socket. Страница Environment Variables описывает `REDIS_HOST`/`REDIS_PORT` как обязательные; при расхождении ориентир — `.env.sample`.
- `PANEL_DOMAIN` (необязательная) — домен панели для прямых ссылок, например в Telegram-уведомлениях.
- Масштабирование: `API_INSTANCES` (по умолчанию `1`, не больше числа ядер CPU; по docs может помочь при 40k+ пользователей). В `remnawave/backend` есть также `docker-compose-advanced-prod.yml`, где REST API и scheduler разнесены в отдельные сервисы; по комментариям в файле REST API масштабировать можно, scheduler — нельзя. Отдельной страницы docs для него нет.

## Environment variables

- Файл `.env` обычно лежит в `/opt/remnawave`.
- При изменении `.env` контейнеры нужно пересоздать, простой restart окружение не меняет:

```bash
docker compose down && docker compose up -d
```

- Remnawave подключается к Postgres через `DATABASE_URL` (`postgresql://{user}:{password}@{host}:{port}/{database}`); `POSTGRES_*` используются контейнером базы, а не самим Remnawave.
- Секреты — случайные строки не короче `64` символов (`openssl rand -hex 64`); значения `change_me` в production недопустимы.
- `SUB_PUBLIC_DOMAIN` задаёт публичный URL подписки в ответах REST API и в UI. Если в Subscription Page задан `CUSTOM_SUB_PREFIX`, тот же путь добавляется к `SUB_PUBLIC_DOMAIN`.
- Полный список (Telegram, webhooks, метрики, уведомления, `SHORT_UUID_LENGTH`, `JWT_AUTH_LIFETIME` и другие) — страница Environment Variables в docs.rw.
- В `.env.sample` есть переменные, которых нет на странице docs:
  - `SHORT_UUID_METHOD` — формат идентификатора ссылки подписки: `nanoid` (по умолчанию, длина из `SHORT_UUID_LENGTH`), `uuid` или `custom` (шаблон из `SHORT_UUID_CUSTOM_PATTERN`, 16–64 символа);
  - `SERVICE_SNI_VERIFICATION` (по умолчанию `true`) — Panel при подключении к API Node (`NODE_PORT`, mTLS, TLS 1.3) передаёт SNI, вычисленный из CA-сертификата и публичного ключа этой Panel (вид `<32 hex>.<10 hex>.com`). При `false` SNI не передаётся. Пара к переменной Node `SNI_VERIFICATION` ([nodes.md](nodes.md)): если на Node она включена, а здесь выключена, Panel к Node не подключится.

## Reverse proxy

- Remnawave не поддерживает публикацию на sub-path (например, `location /remnawave {`). Только root path домена или subdomain.
- SSH Port Forwarding не поддерживается; только один из reverse proxy ниже.
- Варианты в docs: `Caddy`, `Nginx`, `Traefik`, `Angie`.
- `TryCloudflare` — только для разработки, не для production.

## Защита панели

Официальная страница Panel Security описывает дополнительные слои защиты:

- `Caddy with minimal setup`;
- `Caddy with custom path`;
- `Cloudflare ZeroTrust` (по docs: SSL Strict, Proxied, Access application с политикой; Cloudflare-side детали — skill `cloudflare`);
- `TinyAuth for Nginx`.

## Типовые сценарии

- Первая установка Panel на новый VPS.
- Перенос старого стенда на официальный `docker-compose-prod.yml`.
- Исправление небезопасной установки, где Panel был опубликован без reverse proxy.

## Ошибки

- Оставить значения `change_me` в секретах.
- Не сменить пароль Postgres.
- Пытаться публиковать Panel на sub-path вроде `/remnawave`.
- Использовать SSH port forwarding как постоянную схему публикации.
- Менять `.env`, а затем просто рестартовать контейнеры без recreate.

## Проверка результата

- `docker compose ps` показывает рабочие контейнеры.
- `docker compose logs -f -t` не показывает постоянных crash-loop ошибок.
- Panel открывается по домену reverse proxy.
- `FRONT_END_DOMAIN` и `SUB_PUBLIC_DOMAIN` согласованы с фактическим доменом.
- Сервисы не торчат наружу напрямую, кроме контролируемой reverse proxy точки входа.
- После первой регистрации первый пользователь становится `super-admin`.
