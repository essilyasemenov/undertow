# Happ Routing

Что официально известно о Happ Routing в Remnawave и где проходят границы.

## Что подтверждено

- В меню панели раздел `Utilities` содержит `Happ Routing` — конструктор для создания и управления routing rules для клиента Happ.
- В `Detailed Info` пользователя есть Happ Crypto links ([users.md](users.md)).
- Отдельной пошаговой страницы со всеми полями, форматом экспорта и примерами правил Happ Routing в docs.rw нет.

## Чем Happ Routing не является

| Механизм | Где действует |
| --- | --- |
| Happ Routing | правила маршрутизации для клиента Happ |
| Server-Side Routing | маршрутизация трафика на Node через Config Profile ([config-profiles.md](config-profiles.md)) |
| Response Rules | какой ответ и Template получает запрос подписки ([subscriptions.md](subscriptions.md)) |

## Практика

1. Убедиться, что задача про Happ Routing, а не про Server-Side Routing, Templates или Response Rules.
2. В панели открыть `Utilities` → `Happ Routing`.
3. Если нужна точная схема полей, формат экспорта или внутренняя логика правил, прямо сказать, что docs.rw её не описывают, и опираться на текущий интерфейс панели.

## Ошибки

- Приписывать Happ Routing шаги `Server-Side Routing`.
- Выдумывать недокументированную схему правил.
- Считать, что docs.rw содержат полное описание полей Happ Routing.
