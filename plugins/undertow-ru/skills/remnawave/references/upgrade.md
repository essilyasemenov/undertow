# Обновление и переход со старых версий

Только для уже работающей установки. Новая установка с нуля: [install.md](install.md).

## Сначала определить версии

Сценарий зависит от того, с какой версии обновляется установка. Не считать по умолчанию, что это переход 2.x → 3.x, и не считать, что это обновление внутри 3.x.

1. Если пользователь назвал версию, использовать её.
2. Если не назвал, сначала спросить или предложить проверить:
   - тег образа в `docker-compose.yml` Panel: в текущем официальном файле это `remnawave/backend:3`, то есть мажорная версия 3; тег `latest` версию не говорит;
   - версии Remnawave Node и `Xray-core` показаны в карточке Node в Panel (`Nodes` → `Management`).

   ```bash
   cd /opt/remnawave && grep -n 'image:' docker-compose.yml
   ```

3. Дальше один из сценариев:

| Текущая версия | Сценарий |
| --- | --- |
| 3.x, обновление до более новой 3.x | раздел «Обновление в пределах 3.x» и changelog за пропущенные релизы |
| 2.x → 3.x | раздел «Переход с 2.x на 3.x» |
| неизвестна | ответ ограничить шагом определения версии (и при нестандартной установке — [discovery.md](discovery.md)); команды обновления и таблицу 2.x → 3.x не приводить, пока версия не выяснена |

## Обновление в пределах 3.x

Каталоги ниже — из официальной установки; для нестандартной сначала [discovery.md](discovery.md).

Docs рекомендуют обновлять сначала Panel, затем Nodes. Изменения между релизами описывает changelog (`https://docs.rw/changelog`).

Panel:

```bash
cd /opt/remnawave && docker compose pull && docker compose down && docker compose up -d && docker compose logs -f
docker image prune
```

Node:

```bash
cd /opt/remnanode && docker compose pull && docker compose down && docker compose up -d && docker compose logs -f
```

Subscription Page:

```bash
cd /opt/remnawave/subscription && docker compose pull && docker compose down && docker compose up -d && docker compose logs -f
```

## Переход с 2.x на 3.x

Отличия текущих файлов `remnawave/backend` от материалов для 2.x:

| Было в материалах для 2.x | Сейчас в `.env.sample` и `docker-compose-prod.yml` |
| --- | --- |
| `JWT_AUTH_SECRET`, `JWT_API_TOKENS_SECRET` | один `APP_SECRET` |
| `IS_DOCS_ENABLED`, `SWAGGER_PATH`, `SCALAR_PATH` | отсутствуют |
| — | Valkey (`valkey/valkey`), связь через `REDIS_SOCKET` |
| — | необязательная `PANEL_DOMAIN` |

- Пошаговой процедуры миграции 2.x → 3.x страницы docs.rw не содержат. Её источник — changelog и release notes; без них шаги миграции не выдумывать.
- После правки `.env` контейнеры пересоздаются (`docker compose down && docker compose up -d`), простой restart окружение не меняет.
- Резервная копия `.env`, `docker-compose.yml` и базы перед мажорным обновлением — общая практика, а не шаг из docs.rw.

## Ошибки

- Выдавать сценарий 2.x → 3.x, не выяснив текущую версию, или наоборот.
- Обновлять Nodes раньше Panel.
- Переносить в 3.x переменные `JWT_AUTH_SECRET`, `JWT_API_TOKENS_SECRET` из старых гайдов.
- Перезапускать контейнеры после правки `.env` без recreate.
- Пропускать changelog между мажорными версиями.

## Проверка результата

- `docker compose ps` показывает рабочие контейнеры.
- `docker compose logs -f` не показывает постоянных ошибок после старта.
- Nodes в Panel подключены, Xray запущен (`docker exec remnanode xlogs` на Node).
