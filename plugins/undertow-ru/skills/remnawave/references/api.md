# REST API

API Tokens, встроенная документация API, структура контроллеров и безопасная работа с официальной спецификацией.

## Теория

- Официальная интерактивная документация API: `https://docs.rw/api`.
- Префикс всех маршрутов — `/api`; авторизация — `Authorization: Bearer <token>`.
- `API Tokens` с версии 2.2.0 находятся в `Remnawave Settings`.
- Токены поддерживают scopes: права на ресурс в формате `<ресурс>:read`, `<ресурс>:write` или `<ресурс>:*`. Список доступных scopes отдаёт `GET /api/tokens/scopes`.
- Ресурсы scopes (`libs/contract/api/controllers-info.ts`): `users` (включая bulk-операции), `hwid-user-devices`, `subscription`, `subscriptions`, `nodes`, `node-plugins`, `node-ssh`, `node-integrations`, `bandwidth-stats`, `connections`, `config-profiles`, `internal-squads`, `external-squads`, `hosts`, `subscription-template`, `subscription-settings`, `infra-billing`, `system`, `keygen`, `subscription-request-history`, `snippets`, `remnawave-settings`, `subscription-page-configs`, `metadata`, `auth`, `passkeys`, `api-tokens`. Например, токен только на чтение пользователей — `users:read`.
- При создании токена (`POST /api/tokens`) обязательны `name` (2–30 символов) и `expiresInDays` (≥ 1). Если `scopes` не передать, по умолчанию выдаётся `["*"]` — полный доступ.
- Публичный контроллер подписки `/api/sub/...` не требует авторизации и предназначен только для запросов клиентов.

## Встроенная документация

В 3.x переменных `IS_DOCS_ENABLED`, `SWAGGER_PATH` и `SCALAR_PATH` больше нет. Panel всегда публикует:

- Swagger UI: `/api/backend-tools/swagger`;
- Scalar: `/api/backend-tools/scalar`.

Оба пути закрыты отдельной авторизацией backend tools (cookie, подписанная `APP_SECRET`). Как получить доступ из интерфейса панели, docs не описывают; это видно только в коде `remnawave/backend`.

## Контроллеры

Маршруты `remnawave/backend` 3.4.11 (`libs/contract/api`), все под `/api`:

| Контроллер | Путь |
| --- | --- |
| Users | `users` |
| API Tokens | `tokens` |
| Hosts | `hosts` |
| Config Profiles | `config-profiles` |
| Nodes | `nodes` |
| Node Plugins | `node-plugins` |
| Internal / External Squads | `internal-squads`, `external-squads` |
| Snippets | `snippets` |
| Subscriptions (защищённый) | `subscriptions` |
| Подписка (публичный) | `sub` |
| Subscription Templates / Settings | `subscription-templates`, `subscription-settings` |
| Subscription Page configs | `subscription-page-configs` |
| Subscription Request History | `subscription-request-history` |
| HWID | `hwid` |
| Remnawave Settings | `remnawave-settings` |
| System, Auth, Keygen, Metadata, Bandwidth stats, Infra billing | `system`, `auth`, `keygen`, `metadata`, `bandwidth-stats`, `infra-billing` |
| Connections, Node SSH, Node integrations, Passkeys | `connections`, `node-ssh`, `node-integrations`, `passkeys` |

## Примеры операций

Подтверждены в контракте backend:

- `GET /api/tokens`, `POST /api/tokens`, `DELETE /api/tokens/{uuid}`, `GET /api/tokens/scopes`;
- `GET /api/users`, `POST /api/users`, `PATCH /api/users`, `GET /api/users/{id}`, `DELETE /api/users/{id}`;
- `GET /api/users/by-username/{username}`, `GET /api/users/by-short-uuid/{shortUuid}`;
- `POST /api/users/{id}/actions/enable`; рядом `disable`, `reset-traffic`, `revoke`, `extend` (методы остальных — в спецификации);
- массовые операции `POST /api/users/bulk/...` (`update`, `delete`, `reset-traffic`, `extend-expiration-date`, `update-squads` и др.);
- `GET /api/hosts`, `POST /api/hosts`, `PATCH /api/hosts`, `GET /api/hosts/{uuid}`;
- `GET /api/config-profiles`.

Маршруты пользователя адресуются по числовому `id` (`userId`), Hosts и токены — по `uuid`. Точное тело запроса и DTO ответа описаны в официальной спецификации и могут меняться между версиями.

## SDK

Официальные SDK описаны в docs.rw (раздел SDK): TypeScript, Python, Go, а также XTLS-SDK для работы с Xray. Контракт API — источник истины, SDK — обёртки над ним.

## Практика

1. Создать API Token в `Remnawave Settings` с минимально нужными scopes.
2. Определить класс операций: публичная подписка, защищённые admin-операции, settings/tokens/tooling.
3. Метод, тело и ответ — по официальной спецификации; локальный справочник их не фиксирует.
4. Для automation и Subscription Page использовать токен через переменную окружения (`REMNAWAVE_API_TOKEN`), не вписывать его в код.

## Ошибки

- Включать встроенную документацию через `IS_DOCS_ENABLED` в 3.x: переменной больше нет.
- Придумывать endpoint, которых нет в официальной спецификации.
- Подставлять `uuid` пользователя в маршруты, где нужен числовой `id`.
- Создавать токен без `scopes`: по умолчанию это полный доступ.
- Выдавать токену все scopes, когда хватает чтения.
- Смешивать публичный `/api/sub` и защищённые admin-операции.
- Фиксировать request/response schema вручную без сверки со спецификацией.
