# Nodes

Deployment и подключение Remnawave Node, node firewall, назначение Config Profile, operational card, официально описанные advanced-практики и Node Plugins.

## Теория

Официальная документация определяет `Remnawave Node` как lightweight container, который включает `Xray-core`. Panel не включает `Xray-core`, поэтому полноценная эксплуатация Remnawave требует Node.

Guide `Nodes` прямо предупреждает, что не покрывает установку: install-шаги берутся со страницы `Remnawave Node`, а интерпретация UI — из learning materials. Не смешивать install и dashboard semantics.

## Установка Node

1. Убедиться, что на node server установлен Docker с Compose plugin.
2. Создать каталог:

   ```bash
   mkdir /opt/remnanode && cd /opt/remnanode
   ```

3. В Panel открыть `Nodes` → `Management` и нажать `+`.
4. Заполнить форму. `Node Port` — порт, на котором Node принимает internal API requests от Panel; ни для чего другого он не используется.
5. Нажать `Copy docker-compose.yml`.
6. Создать `docker-compose.yml` на node server и вставить содержимое:

   ```bash
   cd /opt/remnanode && nano docker-compose.yml
   ```

7. Запустить:

   ```bash
   docker compose up -d && docker compose logs -f -t
   ```

8. Вернуться в Panel, нажать `Next`, выбрать `Config Profile` и нажать `Create`.
9. Закрыть `NODE_PORT` firewall-правилом, разрешив его только для IP панели.

В скопированном `docker-compose.yml` Node работает с `network_mode: host`, а `NODE_PORT` и `SECRET_KEY` передаются через `environment`. `SECRET_KEY` можно получить и через Rescue CLI панели ([troubleshooting.md](troubleshooting.md)).

### Проверка SNI на `NODE_PORT`

Переменная Node `SNI_VERIFICATION` (по умолчанию `false`, задаётся в `environment` в `docker-compose.yml` Node):

- при `true` Node принимает TLS-рукопожатие на `NODE_PORT` только с SNI, вычисленным из CA-сертификата и публичного ключа Panel из `SECRET_KEY`; с другим SNI или без него соединение обрывается до выдачи сертификата Node (`unknown sni`). Сканер, который не знает этот SNI, не видит сертификат API Node;
- ожидаемый SNI Node печатает в логе при старте, в блоке `SECRET_KEY OK`;
- Panel передаёт этот SNI, только если у неё `SERVICE_SNI_VERIFICATION=true` (значение по умолчанию, [install.md](install.md)). Включать `SNI_VERIFICATION` на Node при выключенной проверке на Panel нельзя: Panel не подключится.

В docs.rw эти переменные не описаны; поведение установлено по исходному коду `remnawave/backend` 3.4.11 и `remnawave/node` 3.4.6.

## Operational card

Guide `Nodes` описывает:

- `Node Vitals`: Country, Internal name, Address (IP или домен Node), Port;
- `Consumption`: multiplier для учёта user traffic (`1.0` — обычный учёт, `0.5` и `2.0` меняют биллинг-эквивалент);
- `Core Configuration`: выбор `Config Profile`. На одну Node — **только один** Profile, так как профиль — это полная конфигурация `Xray-core`; внутри профиля можно активировать несколько `Inbounds`;
- `Tracking & Billing`: `Infrastructure Provider`, `Track traffic usage`, `Traffic limit`, `Reset day`, `Notification %`. Panel записывает трафик всегда; флажок включает контроль относительно лимита;
- `Node Management` и индикаторы статуса: число подключений (дубликаты учитываются), версия `Xray-core`, версия Remnawave Node;
- блок `Actions`: `Update`, `Restart all nodes`;
- `More actions`: `Show usage`, `Copy Node UUID`, `Disable`, `Delete`.

## Advanced usage

### Свои geosite и geoip

- Дополнительные файлы монтируются в `/usr/local/share/xray/` внутри контейнера, **каждый файл отдельно**. Монтирование всей папки перезапишет стандартные geosite/geoip.
- В Xray config файл вызывается как `ext:<файл>.dat:<категория>`.
- Routing на Node управляет серверным трафиком и не влияет на клиентские `DIRECT`-соединения; клиентскую маршрутизацию настраивают на клиенте.

### Логи Node на хосте

- Смонтировать `/var/log/remnanode` в контейнер и указать пути в секции `log` Xray config (`error.log`, `access.log`).
- Обязательно настроить `logrotate`, иначе логи заполнят диск:

```bash
mkdir -p /var/log/remnanode
sudo apt update && sudo apt install logrotate
nano /etc/logrotate.d/remnanode
logrotate -vf /etc/logrotate.d/remnanode
```

Пример конфигурации из docs: `size 50M`, `rotate 5`, `compress`, `missingok`, `notifempty`, `copytruncate`.

### TLS-сертификаты для Xray

- Нужны для TLS-транспорта (например, `VLESS-Vision-TLS`); для Reality не нужны.
- Сертификаты монтируются **в контейнер Panel** в каталог `/var/lib/remnawave/configs/xray/ssl/`. При отправке конфигурации Panel сама читает файлы и передаёт сертификаты на Node.
- В Xray config ссылаться на внутренний путь, например `/var/lib/remnawave/configs/xray/ssl/privkey.key` и `fullchain.pem`; следить за расширениями `.key` и `.pem`.

## Node Plugins (β)

Дополнительные модули на Node: **Torrent Blocker**, **Ingress Filter**, **Egress Filter**, настройка **Connection Drop**, общие списки **Shared Lists**. Доступны с Panel и Node `v2.7.0`. Есть также **Pre Start** (Cleanup Sockets: удаляет указанные socket-файлы при старте Xray, нужен Node `v3.0.0`) и **Executor** (команды: временная блокировка и разблокировка IP, сброс таблицы `nftables`; плагины не обязательны, но нужен `NET_ADMIN`).

Требования:

- в `docker-compose.yml` Node директива `cap_add: NET_ADMIN`;
- на хосте `nftables` (`nft --version`);
- ядро Linux `5.7` или выше (`uname -r`).

Плагины Torrent Blocker, Ingress Filter и Egress Filter работают напрямую с firewall сервера: Node создаёт таблицу `ip remnanode` в `nftables`.

| Плагин | Что делает | Важно |
| --- | --- | --- |
| Torrent Blocker | Блокирует на `blockDuration` секунд IP, с которого обнаружен torrent-трафик; добавляет своё правило первым в `routing.rules` | Нужен `Xray-core` ≥ `26.3.27` и `sniffing` с `destOverride` (`http`, `tls`, `quic`) на inbound |
| Ingress Filter | Постоянно блокирует входящий трафик с IP/CIDR из списка | Docs называют его очень опасным инструментом |
| Egress Filter | Блокирует исходящие подключения к IP/CIDR и портам (например, 25, 465, 587) | — |
| Connection Drop | Whitelist IP для автоматического сброса соединений при удалении пользователя | Сброс работает всегда с `NET_ADMIN` (с Node `v2.6.0`); whitelist нужен, например, для мостов |
| Shared Lists | Именованные списки IP для других плагинов | Формат `ext:<имя>`, тип `ipList` |

Поля у каждого плагина свои, `enabled` (по умолчанию выключен) есть у всех:

| Плагин | Поля |
| --- | --- |
| `torrentBlocker` | `ignoreLists.ip` (без CIDR), `ignoreLists.userId`, `blockDuration` (секунды), `includeRuleTags` (необязательно: блокировать и по своим правилам с `ruleTag`) |
| `ingressFilter` | `blockedIps` (IP/CIDR, IPv4/IPv6) |
| `egressFilter` | `blockedIps`, `blockedPorts` |
| `connectionDrop` | `whitelistIps` |
| `sharedLists` | `name`, `type`, `items` |

Где именно в UI Panel редактируется конфигурация плагинов, текст docs не описывает (показано только на скриншоте).

## Типовые сценарии

- Первое подключение одной Node к Panel.
- Назначение нового Config Profile на Node.
- Настройка traffic coefficient для billing semantics.
- Включение node-side limit tracking с monthly reset.
- Подключение geosite/geoip mount-ов к Node.
- Вынос node logs на host filesystem с `logrotate`.
- Передача TLS certificate files в Node через Panel.
- Блокировка torrent или нежелательных исходящих портов через Node Plugins.

## Ошибки

- Открыть `NODE_PORT` во внешний интернет.
- Монтировать весь каталог `/usr/local/share/xray/`, перезаписывая дефолтные geosite/geoip files.
- Подключить logs без log rotation.
- Считать, что server-side routing влияет на клиентские `DIRECT` connections.
- Монтировать TLS-сертификаты в контейнер Node вместо Panel.
- Включать Torrent Blocker без `sniffing` на inbound.
- Включать плагины без `cap_add: NET_ADMIN`.
- Игнорировать `Consumption` multiplier и неверно интерпретировать фактический расход user traffic.

## Проверка результата

- Node отображается в `Nodes` → `Management`.
- Для Node выбран нужный `Config Profile`.
- `docker compose logs -f -t` на node server не показывает постоянных ошибок.
- `NODE_PORT` доступен только с IP Panel.
- При необходимости настроены `Consumption` и `Tracking & Billing`.
- Для плагинов: таблица `remnanode` видна в `nft list ruleset`.
