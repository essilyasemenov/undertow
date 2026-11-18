---
name: remnawave
description: "Remnawave 3.x (панель управления прокси на Xray-core): установка Panel и Node, docker compose, .env (APP_SECRET, FRONT_END_DOMAIN, SUB_PUBLIC_DOMAIN, PANEL_DOMAIN), Valkey/Redis, reverse proxy (Caddy, Nginx, Traefik, Angie), защита панели, обновление (upgrading), Nodes, NODE_PORT, SECRET_KEY, Node Plugins (Torrent Blocker, Ingress/Egress Filter, Connection Drop, Shared Lists), Config Profiles, Xray JSON, inbounds, snippets, Internal Squads, Hosts, server-side routing и каскад (bridge) между Nodes, troubleshooting (SPAWN_ERROR, xlogs, Rescue CLI), Users, Internal и External Squads, HWID device limit, подписки (Subscription URL, Hosts, Templates Mihomo/Xray-json/Sing-box/Base64, Response Rules, Subscription Page, injectHosts), REST API и API Tokens со scopes, Happ Routing, поиск фактических файлов установки на сервере (где лежит .env, docker-compose.yml, конфиги, контейнеры панели и ноды, нестандартная установка). Использовать для любых задач по Remnawave Panel и Node только по docs.rw и github.com/remnawave."
license: MIT
---
# remnawave

Общий вход в задачи по Remnawave. Отвечать на русском языке.

Remnawave — инструмент управления прокси поверх `Xray-core`. Компоненты по официальной документации: Panel (главная точка входа), Backend (NestJS), Frontend (React), Node (лёгкий контейнер с `Xray-core`), XTLS-SDK, XTLS-SDK-NestJS. Panel не содержит `Xray-core`, поэтому для работы нужна хотя бы одна Node.

Цепочка установки из quick start: Remnawave Panel → Reverse Proxy → Subscription Page (опционально) → Remnawave Node.

## Как работать с этим skill

1. Определить область задачи: установка, обновление, Nodes, Config Profiles, пользователи, подписки, API, Happ Routing или диагностика.
   - Новая установка и обновление — разные операции. Если из вопроса не следует, что Remnawave уже работает, считать установку новой и не упоминать старые версии, миграцию и устаревшие переменные.
   - Обновление — только когда пользователь об этом говорит или видна существующая установка. Сначала выяснить, с какой версии и до какой обновляются: обновление внутри 3.x и переход 2.x → 3.x — разные сценарии ([upgrade.md](references/upgrade.md)).
2. Зафиксировать version-sensitive контекст:
   - какой release Panel и Node используется;
   - где размещены Panel и Node;
   - есть ли reverse proxy;
   - нужен UI workflow или REST API workflow.
3. Panel и Node работают на серверах пользователя. Если Claude Code запущен не на этом сервере (обычно так и есть), не искать файлы Remnawave на локальном диске и не читать домашний каталог пользователя: дать команды, которые пользователь выполнит на сервере сам.
4. Пути и имена контейнеров в справочниках — из официальной установки (`/opt/remnawave`, `/opt/remnanode`, контейнеры `remnawave`, `remnanode`). Если работа идёт с существующим сервером и пользователь не подтвердил, что установка официальная, сначала предложить команды обнаружения из [discovery.md](references/discovery.md) и подставлять фактические каталоги и имена.
5. Открыть нужный раздел и не додумывать неподтверждённые функции, параметры или шаги UI.
6. Не выполнять production-изменение, пока шаг не подтверждён официальной документацией.

## Разделы (`references/`)

| Задача | Файл |
| --- | --- |
| Существующий сервер: где фактически лежат compose-файлы, `.env`, какие контейнеры и порты | [discovery.md](references/discovery.md) |
| Новая установка: требования, Panel, `.env`, reverse proxy, защита панели | [install.md](references/install.md) |
| Обновление и переход с 2.x на 3.x | [upgrade.md](references/upgrade.md) |
| Установка Node, firewall, operational card, geo-файлы, логи, TLS-сертификаты, Node Plugins | [nodes.md](references/nodes.md) |
| Config Profiles, цепочка активации inbound, snippets, server-side routing и каскад | [config-profiles.md](references/config-profiles.md) |
| Users, Internal и External Squads, Bulk Actions, HWID device limit | [users.md](references/users.md) |
| Подписка: Hosts, Templates, Response Rules, Subscription Page | [subscriptions.md](references/subscriptions.md) |
| REST API, API Tokens и scopes, встроенная документация | [api.md](references/api.md) |
| Happ Routing и его границы | [happ-routing.md](references/happ-routing.md) |
| Диагностика: слои сбоя, логи Xray, частые ошибки, Rescue CLI | [troubleshooting.md](references/troubleshooting.md) |
| Официальные ссылки | [sources.md](references/sources.md) |

## Рабочий порядок

```text
remnawave task
  -> classify scope
    -> confirm official source
      -> choose reference
        -> check version-sensitive behavior
          -> apply only documented workflow
```

## Правила качества

- Источники фактов: только `docs.rw` и `github.com/remnawave`. Синтаксис и поведение самого Xray — официальная документация Xray (`xtls.github.io`).
- Если функция, endpoint, элемент интерфейса или поведение в эксплуатации не подтверждены, явно отмечать отсутствие подтверждения.
- Не смешивать установку, API и настройку подписок в один непроверенный ответ.
- Для задач, критичных для production, учитывать reverse proxy, то, какие сервисы открыты наружу, и поведение конкретной версии.
- Материал сверен с Remnawave backend `3.4.11` (подробности в [sources.md](references/sources.md)). Изменения в более новых релизах описывает changelog.
- Не путать Happ Routing и Server-Side Routing: официальные материалы различают эти вещи.

## Связь с другими skills

- DNS, routing, MTU, reverse proxy, firewall, TLS, Linux networking: skill `network`.
- Публикация Panel, подписок и Node через Cloudflare: skill `cloudflare`.
- Выбор топологии (direct, cascade, CDN, WARP): skill `architecture`.
- Перед финальным решением по Nodes, Hosts и маршрутизации пройти skill `detection-audit`.
