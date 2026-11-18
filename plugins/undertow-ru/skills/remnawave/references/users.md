# Users и Squads

Создание и сопровождение Users, лимиты, срок подписки, Internal и External Squads, HWID device limit.

## Теория

Пользователь в Remnawave получает Subscription URL и набор ограничений:

- `Data limit` — квота трафика в GB;
- `Traffic reset strategy` — как часто обнуляется счётчик;
- срок окончания подписки;
- один или несколько `Internal Squads` (что доступно);
- при необходимости `External Squad` (что и как выдаётся в подписке).

Первый зарегистрированный пользователь панели становится `super-admin`. Забытый пароль восстанавливается через Rescue CLI ([troubleshooting.md](troubleshooting.md)).

## Создание пользователя

1. `Users` → `Create user`.
2. Username — любой, но без пробелов.
3. `Traffic & Limits`: `Data limit`, `Traffic reset strategy`.
4. `Access Settings`: дата окончания подписки, один или несколько `Internal Squads`, при необходимости `External Squad`.
5. `Create user`.

Subscription URL копируется иконкой ссылки в списке или берётся в `Edit user`. В браузере по нему открывается Subscription Page.

## Инструменты пользователя

`Edit user` (иконка карандаша) → `More actions`:

| Пункт | Что показывает |
| --- | --- |
| `Detailed Info` | дополнительные данные, в том числе VLESS UUID и Happ Crypto links |
| `Show usage` | подробная статистика трафика |
| `HWIDs and Devices` | устройства, о которых сообщили клиентские приложения (не все клиенты это поддерживают) |
| `Subscription QR Code` | QR-код Subscription URL |
| `Subscription links` | сырые ссылки `vless://`, `ss://` и т. п. |
| `Request History` | запросы клиентских приложений за подпиской |

В разделе `Tools` есть также `HWID Inspector` (HWID от клиентов) и `SRH Inspector` (анализ запросов подписки).

## Bulk Actions

Красная кнопка с шестерёнкой справа на странице `Users`. Действует на всех пользователей или на выбранных (чекбоксы, фильтры): включить/выключить, единый лимит и стратегия сброса, продление подписки и другое.

## Internal Squads

- Internal Squad — группа доступа: какие Inbounds доступны её участникам. Можно выбрать Inbounds из любых Config Profiles.
- Пользователь может состоять в нескольких Internal Squads (например, «regular» и «premium»).
- Создание: `Internal Squads` → `+` или `Edit` у существующего.
- Стрелка рядом с `Edit`: `Add users` (добавить всех), `Remove users` (убрать всех), `View accessible nodes` (какие Nodes доступны участникам).

## External Squads

- С версии 2.2.0. Переопределяют то, что получают пользователи в подписке: Templates и настройки из `Subscription` → `Settings` (например, `Announce`).
- Пример из docs: отдельные External Squads для разных стран со своими Templates.
- Создание: `External Squads` → `+`; вкладки `Templates` и `Settings`.
- Response Rules имеют приоритет над External Squads ([subscriptions.md](subscriptions.md)).

## HWID device limit

- Ограничивает число устройств, которые могут добавить подписку. Необязательный, по умолчанию выключен.
- Настройка: `Subscription` → `Settings` → `HWID Device Limit`; можно переопределить для External Squad.
- Лимит по умолчанию (fallback) задаётся там же, в `Subscription` → `Settings` → `HWID Device Limit` (в API — `hwidSettings.fallbackDeviceLimit`); там же `maxDevicesAnnounce` — сообщение пользователю при достижении лимита. Страница docs называет его `HWID_FALLBACK_DEVICE_LIMIT`, но в 3.4.11 такой переменной окружения нет: в `.env` её не прописывать.
- Для пользователя: свой лимит (иначе действует fallback) или отключение лимита.
- Работает только с клиентами, которые присылают заголовок HWID. Если лимит включён, а клиент заголовок не шлёт, Remnawave отвечает `404` и подписку получить нельзя, пока лимит для пользователя не отключён.
- Клиенты с поддержкой по docs: Happ, v2RayTun, форки сообщества (Koala Clash, FlClashX, Prizrak-Box), Incy, RenoarX, DeskBox, Passwall; у Throne, Shadowrocket, Clash Mi, Karing поддержка выключена по умолчанию.
- Заголовки: `x-hwid`, `x-device-os`, `x-ver-os`, `x-device-model`. С Panel 3.0.0 `x-hwid` должен соответствовать `^[a-zA-Z0-9=-]{10,64}$`, иначе игнорируется.
- Заголовки ответа подписки показывают, почему клиент получил отказ:
  - `x-hwid-active: true` — HWID device limit включён в панели;
  - `x-hwid-not-supported: true` — лимит включён, а клиент не прислал `x-hwid`;
  - `x-hwid-max-devices-reached: true` — пользователь достиг лимита устройств;
  - `x-hwid-limit: true` — то же при достигнутом лимите, для обратной совместимости с v2RayTun.
- Rescue CLI умеет удалить все сохранённые HWID-устройства.

## Ошибки

- Использовать пробелы в username.
- Создать пользователя без нужного `Internal Squad`: доступ к Inbounds окажется неполным.
- Включить HWID device limit, не проверив клиенты пользователей: клиенты без HWID получат `404`.
- Прописывать `HWID_FALLBACK_DEVICE_LIMIT` в `.env`: в 3.x лимит настраивается в панели.
- Ждать, что External Squad перекроет Response Rule: приоритет у Response Rules.
- Считать `Detailed Info` или `HWIDs and Devices` источником полей, которых нет в docs.

## Проверка результата

- Пользователь виден в списке `Users`, статусы `Total`, `Active`, `Expired` корректны.
- Subscription URL открывается в браузере.
- Клиент после импорта подписки подключается к Node.
