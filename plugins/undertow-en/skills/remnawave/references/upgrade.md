# Upgrading and moving from old versions

Only for an installation that is already running. A fresh installation: [install.md](install.md).

## Determine the versions first

The scenario depends on which version the installation is upgraded from. Do not assume by default that it is a move from 2.x to 3.x, and do not assume it is an upgrade within 3.x.

1. If the user named a version, use it.
2. If not, ask first or suggest checking:
   - the image tag in the Panel's `docker-compose.yml`: in the current official file it is `remnawave/backend:3`, i.e. major version 3; the `latest` tag does not tell the version;
   - the Remnawave Node and `Xray-core` versions are shown on the Node card in Panel (`Nodes` → `Management`).

   ```bash
   cd /opt/remnawave && grep -n 'image:' docker-compose.yml
   ```

3. Then one of the scenarios:

| Current version | Scenario |
| --- | --- |
| 3.x, upgrading to a newer 3.x | the section "Upgrading within 3.x" and the changelog for the skipped releases |
| 2.x → 3.x | the section "Moving from 2.x to 3.x" |
| unknown | limit the answer to the step of determining the version (and, for a non-standard installation, [discovery.md](discovery.md)); do not give upgrade commands or the 2.x → 3.x table until the version is known |

## Upgrading within 3.x

The directories below come from the official installation; for a non-standard one, see [discovery.md](discovery.md) first.

The docs recommend upgrading Panel first, then Nodes. The changelog (`https://docs.rw/changelog`) describes the changes between releases.

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

## Moving from 2.x to 3.x

Differences between the current `remnawave/backend` files and the 2.x materials:

| In the 2.x materials | Now in `.env.sample` and `docker-compose-prod.yml` |
| --- | --- |
| `JWT_AUTH_SECRET`, `JWT_API_TOKENS_SECRET` | a single `APP_SECRET` |
| `IS_DOCS_ENABLED`, `SWAGGER_PATH`, `SCALAR_PATH` | absent |
| — | Valkey (`valkey/valkey`), connected through `REDIS_SOCKET` |
| — | optional `PANEL_DOMAIN` |

- The docs.rw pages do not contain a step-by-step 2.x → 3.x migration procedure. Its source is the changelog and release notes; do not invent migration steps without them.
- After editing `.env`, the containers are recreated (`docker compose down && docker compose up -d`); a plain restart does not change the environment.
- Backing up `.env`, `docker-compose.yml` and the database before a major upgrade is general practice, not a step from docs.rw.

## Mistakes

- Giving the 2.x → 3.x scenario without finding out the current version, or the other way round.
- Upgrading Nodes before Panel.
- Carrying the variables `JWT_AUTH_SECRET`, `JWT_API_TOKENS_SECRET` from old guides into 3.x.
- Restarting containers after editing `.env` without recreating them.
- Skipping the changelog between major versions.

## Checking the result

- `docker compose ps` shows running containers.
- `docker compose logs -f` shows no persistent errors after startup.
- Nodes are connected in Panel, and Xray is running (`docker exec remnanode xlogs` on the Node).
