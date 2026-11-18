# Config Profiles

Создание Config Profiles, работа с Inbounds, цепочка активации профиля на Node, Host и Squad, snippets и server-side routing (каскад между Nodes).

## Теория

Официальная документация определяет `Config Profile` как полный `Xray-core` configuration template для Node. Профиль содержит все Inbounds и общие настройки, которые нужны Node.

Docs одновременно предупреждают:

- статьи Remnawave не обучают самой настройке `Xray-core`;
- синтаксис и поведение Xray описаны в официальной документации Xray (`xtls.github.io/config`).

Remnawave намеренно очищает массив `clients` в конфигурации Node: пользователей в inbound подставляет сама Panel. Это не ошибка.

## Создание профиля

1. Открыть `Config Profiles` и нажать `Create Config Profile`.
2. Ввести имя профиля.
3. В открывшемся editor:
   - добавить или удалить `Inbounds`;
   - скорректировать остальные Xray settings.
4. При необходимости использовать `Load from GitHub` для шаблона.
5. Сохранить профиль и вернуться в список. Под именем профиля: левая иконка — число `Inbounds`, правая — число `Nodes`, использующих профиль.

## Цепочка активации

Чтобы новый inbound реально дошёл до пользователя, docs описывают такую последовательность:

1. Создать или изменить `Config Profile`.
2. Назначить профиль на Node: `Nodes` → `Management` → карточка Node → `Change Profile`.
3. Включить нужные `Inbounds` на этой Node.
4. На `Hosts` назначить конкретный inbound из профиля.
5. В `Internal Squads` (например, `Default-Squad`) включить этот inbound.

Если последний шаг пропущен, пользователь не получит доступ к новому inbound даже при корректных Node и Host настройках.

## Snippets

- Snippet — заранее определённый массив объектов `"outbounds"` или `"routing"` (правил), который применяется во всех профилях. Удобно, когда у многих профилей одинаковые правила.
- Меню snippets открывается кнопкой `{ }` внизу editor → `+ New snippet`. Содержимое обязательно в квадратных скобках `[]`.
- В Xray JSON snippet подключается объектом `{ "snippet": "<имя>" }`, например внутри `routing.rules`.

## Server-side routing (каскад, bridge)

Docs показывают демонстрационную (не production-ready) схему с двумя Nodes `RU` и `DE`: пользователи подключаются к `RU`, трафик к `.ru` выходит напрямую с `RU`, остальное уходит через `DE`. Такую схему docs называют bridge.

1. **Профиль для DE.** Отдельный Config Profile (например, `DE Bridge Profile`) с inbound для моста (в примере `shadowsocks`, tag `BRIDGE_DE_IN`, порт `9999`, `network: tcp,udp`, sniffing включён) и outbounds `DIRECT` (`freedom`), `BLOCK` (`blackhole`). Назначить профиль на Node `DE` и выбрать `BRIDGE_DE_IN`.
2. **Internal Squad для моста.** Создать, например, `Bridge Squad` и включить в нём `BRIDGE_DE_IN`.
3. **Service user.** Создать пользователя (например, `bridge_user`) с `Data Limit` = `0` и `Expiry Date` в далёком будущем, назначить ему `Bridge Squad`. Пароль взять из карточки пользователя: `More Actions` → `Detailed Info` → `Connection Information` (Trojan Password, VLESS UUID или SS Password — по протоколу inbound).
4. **Публичный профиль RU.** В профиль, к которому подключаются пользователи, добавить outbound на DE (в примере `SS_OUTBOUND_TO_DE`: адрес Node DE, порт `BRIDGE_DE_IN`, пароль service user; для Shadowsocks в Remnawave метод всегда `chacha20-ietf-poly1305`) и правила маршрутизации.

Правила Xray обрабатываются сверху вниз. Порядок из примера:

1. `geoip:private` → `BLOCK`;
2. `geosite:private` → `BLOCK`;
3. `bittorrent` → `BLOCK`;
4. `geoip:ru` → `DIRECT` (RU Node — точка выхода);
5. `geosite:category-ru` → `DIRECT`;
6. всё остальное с `PUBLIC_RU_INBOUND` → `SS_OUTBOUND_TO_DE`.

Вместо Shadowsocks для транзита можно использовать VLESS, обновив конфигурацию соответственно. Выбор между таким каскадом, L4-relay и CDN: skill `architecture`.

## Типовые сценарии

- Создать profile `Sample` и добавить второй `VLESS` inbound.
- Активировать новый профиль на существующей Node.
- Расширить доступ пользователей к новым inbound через `Default-Squad`.
- Вынести общие правила маршрутизации в snippet.
- Собрать каскад RU → DE с прямым выходом для российских ресурсов.

## Ошибки

- Считать Config Profile самодостаточным без назначения на Node.
- Пытаться назначить на одну Node несколько профилей: допускается только один.
- Назначить inbound на Host, но забыть включить его в `Internal Squad`.
- Вписывать пользователей в `clients` вручную: Remnawave очищает этот массив.
- Ставить fallback-правило выше конкретных правил: Xray проверяет правила сверху вниз.
- Ограничивать service user по трафику или сроку: мост перестанет работать.
- Использовать guide Remnawave как замену полной документации `Xray-core`.

## Проверка результата

- Новый профиль появился в списке `Config Profiles`.
- У профиля корректно отображается число `Inbounds` и `Nodes`.
- На Node активирован нужный профиль.
- На Host доступен нужный inbound.
- В `Internal Squad` inbound тоже включен.
- Профиль применился без ошибок запуска Xray: `docker exec remnanode xlogs` на Node ([troubleshooting.md](troubleshooting.md)).
