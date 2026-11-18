# Troubleshooting

Диагностика install и runtime проблем Remnawave по официальным предупреждениям и guides, без подмены source-backed анализа догадками.

## Теория

Официальные материалы заранее предупреждают о нескольких классах проблем:

- сервисы нельзя публиковать напрямую в интернет;
- reverse proxy обязателен;
- sub-path не поддерживается;
- env changes требуют recreate containers;
- `NODE_PORT` нужно ограничивать firewall;
- node logs без `logrotate` могут заполнить диск;
- ошибка в Xray JSON профиля не даёт `Xray-core` стартовать на Node.

## Порядок диагностики

1. Определить слой сбоя:
   - install;
   - reverse proxy;
   - env;
   - node connectivity;
   - запуск Xray на Node (Config Profile);
   - subscription delivery.
2. Базовые команды в каталоге сервиса (официально `/opt/remnawave` или `/opt/remnanode`; если установка нестандартная, каталог и имена контейнеров — через [discovery.md](discovery.md)):

   ```bash
   docker compose ps
   docker compose logs -f -t
   ```

3. Если менялся `.env`, выполнить recreate:

   ```bash
   docker compose down && docker compose up -d
   ```

4. Для Node:
   - логи контейнера: `docker compose logs -f -t`;
   - логи `Xray-core`: `docker exec remnanode xlogs`;
   - конфигурация Xray, которую Node фактически получила от Panel: `docker exec -it remnanode cli --dump-config`;
   - firewall для `NODE_PORT` (открыт только для IP панели).
5. Для subscription: проверить `SUB_PUBLIC_DOMAIN` (совпадает с реальным публичным URL подписки).
6. Для потерянного доступа к панели: Rescue CLI.

## Проверка конфигурации Xray на Node

`Xray-core` работает внутри контейнера Node, а конфигурацию отправляет Panel. Команда `xray -test` на хосте здесь не применяется. Проверка по docs: применить профиль и посмотреть логи `Xray-core`:

```bash
docker exec remnanode xlogs
```

## Частые ошибки

### `XML-RPC fault: SPAWN_ERROR: xray`

В логах Node (`cd /opt/remnanode && docker compose logs -f -t`) видны `SPAWN_ERROR: xray`, а затем `Failed to get system stats ... ECONNREFUSED 127.0.0.1:61000`.

- Причина: `Xray-core` не стартовал, чаще всего из-за ошибки в конфигурации.
- Решение:
  1. Посмотреть логи `Xray-core`: `docker exec remnanode xlogs` — обычно там видна причина.
  2. Исправить конфигурацию в Panel (Config Profile) и сохранить.

## Полезные команды

| Задача | Команда |
| --- | --- |
| Rescue CLI панели | `docker exec -it remnawave cli` |
| Перезапуск Panel | `cd /opt/remnawave && docker compose down && docker compose up -d && docker compose logs -f -t` |
| Монитор PM2 в Panel | `docker exec -it remnawave pm2 monit` |
| Rescue CLI Node | `docker exec -it remnanode cli` |
| Логи `Xray-core` | `docker exec remnanode xlogs` |
| Конфигурация Xray на Node | `docker exec -it remnanode cli --dump-config` |
| Перезапуск Node | `cd /opt/remnanode && docker compose down && docker compose up -d && docker compose logs -f -t` |

## Rescue CLI

Встроенный набор команд обслуживания и восстановления (`docker exec -it remnawave cli`):

- **Reset superadmin** — полностью удаляет superadmin; при следующем входе в браузере предложат создать нового.
- **Enable password authentication** — включает вход по паролю, если его случайно отключили через настройки OAuth.
- **Reset certs** — сбрасывает внутренние сертификаты Remnawave. Docs предупреждают не использовать без понимания последствий.
- **Get SECRET_KEY for a Remnawave Node** — показывает `SECRET_KEY` для подключения Node.
- **Fix Collation** — исправляет проблемы collation базы данных.
- **Clean up HWID Devices** — удаляет все сохранённые HWID-устройства пользователей.
- **Clean up SRH Table** — очищает историю запросов подписки (Subscription Request History); помогает, когда таблица сильно разрослась и увеличила базу.

У Node есть свой Rescue CLI (`docker exec -it remnanode cli`) с одной функцией — **Get cold config**: `docker exec -it remnanode cli --dump-config` выводит конфигурацию Xray, полученную Node.

## Типовые сценарии

- Panel не открывается по домену.
- После правки `.env` изменения не применились.
- Node добавлена, но Xray не стартует.
- Subscription Page не может связаться с Panel.
- Потерян доступ superadmin.

## Ошибки

- Искать причину в UI, когда `.env` не был применён через recreate.
- Оставлять `NODE_PORT` open to world.
- Использовать sub-path routing в reverse proxy.
- Включить logs на node без rotation.
- Запускать `xray -test` на хосте Node вместо просмотра `xlogs`.
- Запускать Rescue CLI командой из старых гайдов: актуальная команда — `docker exec -it remnawave cli`.

## Проверка результата

- Выявлен правильный failure domain.
- Устранение опирается на официальные docs warning/steps.
- После исправления сервис либо открывается, либо явно локализован следующий слой сбоя.
