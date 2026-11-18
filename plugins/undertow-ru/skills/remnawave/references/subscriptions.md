# Подписки: Hosts, Templates, Response Rules, Subscription Page

Цепочка выдачи подписки: Subscription URL, Hosts, Templates, `Subscription` → `Settings`, Response Rules, External Squads и Subscription Page.

## Цепочка выдачи

1. Пользователь получает Subscription URL.
2. Браузер или клиентское приложение запрашивает этот URL; Remnawave сам определяет, кто обращается: браузеру отдаёт веб-страницу, клиенту — конфигурацию в подходящем формате.
3. `Hosts` задают точки входа (адрес, порт, связанный inbound).
4. `Templates` определяют формат конфигурации для семейства клиентов.
5. `Response Rules` выбирают, какой ответ и Template получит конкретный запрос.
6. `Subscription` → `Settings` добавляет метаданные для поддерживаемых клиентов (например, `Subscription Name`).
7. `External Squads` переопределяют Templates и настройки для групп пользователей.
8. Subscription Page скрывает домен панели от конечных пользователей.

Response Rules и Templates относятся к выдаче подписки. Это не `Server-Side Routing` на Nodes ([config-profiles.md](config-profiles.md)) и не Happ Routing ([happ-routing.md](happ-routing.md)).

## Hosts

- Host — точка входа, через которую пользователь попадает на Nodes. Клиент получает список Hosts и выбирает один (например, Host «Finland» только с финскими Nodes).
- `Hosts` → `Create new host`:
  - `Host visibility` — показывать ли Host в подписке; выключенный Host клиенты не видят;
  - `Remark` — имя в dashboard;
  - inbound — **ровно один** на Host, выбирается из любого Config Profile; порт подставляется из inbound (в продвинутых конфигурациях может отличаться);
  - `Address` — IP или домен, который указывает на IP нужной Node.
- Docs советуют домен вместо IP: при смене IP достаточно обновить DNS, пользователям не нужно обновлять подписку.
- `Advanced Options` переопределяют параметры inbound (например, `SNI` вместо `serverNames`); пустые поля берутся из inbound. Docs советуют не трогать без необходимости.

## Templates

Семейства форматов:

| Семейство | Для каких клиентов |
| --- | --- |
| `Mihomo` | клиенты на ядре Mihomo (преемник Clash); есть специальные ключи Remnawave для Mihomo |
| `Xray-json` | клиенты на ядре Xray |
| `Sing-box` | клиенты на ядре Sing-box |
| `Base64` | список конфигураций в Base64; Template нет, используется как fallback, если клиент не подошёл под другие форматы |

- С версии 2.2.0 можно создавать несколько Templates для каждого семейства и раздавать их через External Squads или Response Rules.
- Для `XRAY_JSON` есть директива `injectHosts` (с 2.6.3): Panel подставляет outbounds выбранных Hosts в Template (балансировщики, сложный роутинг). Условия: виртуальный Host включён и не скрыт; инжектируемые Hosts включены (по умолчанию берутся скрытые); inbound всех Hosts входит в Squad пользователя. Подробности — статья «Xray JSON Advanced» в docs.
- Какой клиент получает какой Template по User-Agent, универсальной матрицей в docs не описано.

## Response Rules (SRR)

Упорядоченный JSON-набор правил, который backend проверяет для каждого запроса подписки сверху вниз; первое сработавшее правило останавливает проверку. Response Rules переопределяют настройки External Squads.

Поля правила:

| Поле | Значение |
| --- | --- |
| `name` | обязательно, 1–50 символов |
| `description` | до 250 символов |
| `enabled` | обязательно; `false` — правило пропускается |
| `operator` | `AND` (все условия) или `OR` (любое) |
| `conditions` | список условий; пустой — совпадает со всем (для fallback) |
| `responseType` | `MIHOMO`, `CLASH`, `STASH`, `SINGBOX`, `XRAY_JSON`, `XRAY_BASE64`, `BROWSER`, `BLOCK` (403), `STATUS_CODE_404`, `STATUS_CODE_451`, `SOCKET_DROP` |
| `responseModifications` | `subscriptionTemplate`, `headers` (`key`/`value`), `applyHeadersToEnd`, `ignoreHostXrayJsonTemplate`, `ignoreServeJsonAtBaseSubscription`, `disableHwidCheck` |

Условие: `headerName` (по RFC 7230, регистр имени не важен), `operator` (`EQUALS`, `NOT_EQUALS`, `CONTAINS`, `NOT_CONTAINS`, `STARTS_WITH`, `NOT_STARTS_WITH`, `ENDS_WITH`, `NOT_ENDS_WITH`, `REGEX`, `NOT_REGEX`), `value` (1–255 символов), `caseSensitive`. Несколько значений заголовка склеиваются через запятую; если заголовка нет, правило пропускается.

Пример из docs: Happ на Android получает свой Template.

```json
{
  "name": "Happ Android",
  "enabled": true,
  "operator": "AND",
  "conditions": [
    { "caseSensitive": false, "headerName": "user-agent", "operator": "CONTAINS", "value": "happ" },
    { "caseSensitive": false, "headerName": "x-device-os", "operator": "CONTAINS", "value": "android" }
  ],
  "responseType": "XRAY_JSON",
  "responseModifications": { "subscriptionTemplate": "Happ Android" }
}
```

Docs предупреждают: неверные изменения Response Rules могут нарушить работу системы.

## Subscription Page

Отдельный контейнер, который скрывает домен панели от пользователей. Варианты: `Bundled` (на сервере панели) и `Separate server`.

1. В `.env` панели поменять `SUB_PUBLIC_DOMAIN` на домен страницы подписки (без `http`/`https`) и пересоздать контейнеры панели.
2. Создать API Token в `Remnawave Settings` → `API Tokens`.
3. В `.env` Subscription Page (официально `/opt/remnawave/subscription`):
   - `APP_PORT=3010` (контейнер публикуется на `127.0.0.1:3010`);
   - `REMNAWAVE_PANEL_URL` — `http://remnawave:3000` для Bundled или публичный домен панели для Separate server;
   - `REMNAWAVE_API_TOKEN` — созданный токен;
   - `CUSTOM_SUB_PREFIX` — свой путь (тот же путь добавить к `SUB_PUBLIC_DOMAIN`);
   - `TRUST_PROXY` — сколько прокси перед приложением доверять при чтении `X-Forwarded-For`; `1` для одного reverse proxy на том же хосте, больше — если впереди ещё прокси (например, Cloudflare → Nginx → app).
4. `docker compose up -d && docker compose logs -f`, затем reverse proxy на root path домена (sub-path не поддерживается). В существующий Caddyfile добавлять новый блок, не заменять конфиг целиком.
5. Страница доступна по `https://<домен>/<shortUuid>`.

Внешний вид и список приложений настраиваются в `Subpage Builder` в dashboard. Переключатель `Show Connection Keys` показывает сырые ключи; при включённом HWID он не действует; после изменения нужен перезапуск контейнера страницы.

## Ошибки

- Считать Host контейнером для нескольких inbound: на Host только один inbound.
- Путать Templates и Hosts: Host — точка входа, Template — формат.
- Путать Response Rules с `Server-Side Routing` или Happ Routing.
- Не пересоздать контейнеры панели после изменения `SUB_PUBLIC_DOMAIN`.
- Запустить Subscription Page без `REMNAWAVE_API_TOKEN`.
- Публиковать Subscription Page на sub-path вместо `CUSTOM_SUB_PREFIX`.
- Оставить `TRUST_PROXY=1`, когда перед reverse proxy стоит ещё Cloudflare.

## Проверка результата

- Браузер по Subscription URL получает веб-страницу, клиент по тому же URL импортирует конфигурацию.
- Пользователь видит только Hosts с включённым `Host visibility`.
- Subscription Page отдаёт данные по ожидаемому публичному домену.
- Override External Squads и Response Rules прослеживается в выдаваемой подписке.
