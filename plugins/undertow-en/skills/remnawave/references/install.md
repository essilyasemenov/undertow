# Installing Panel

A fresh installation of Remnawave Panel: preparing the server, `.env`, starting the containers, the mandatory reverse proxy and panel protection. Upgrading and moving from old versions: [upgrade.md](upgrade.md).

## Theory

The official documentation describes this installation model:

- Remnawave Panel is the main component;
- Panel and Node require `Docker` with the `Docker Compose plugin`;
- Panel must be published through a reverse proxy;
- Remnawave services must not be exposed to the Internet directly, only on `127.0.0.1`;
- Panel and its components do not support being served on a sub-path.

## Requirements

| | Panel | Node |
| --- | --- | --- |
| OS | Ubuntu or Debian recommended | Ubuntu or Debian recommended |
| RAM | 2 GB minimum, 4 GB recommended | 1 GB minimum |
| CPU | 2 cores minimum, 4 recommended | 1 core minimum |
| Storage | 20 GB | — |

- Panel can run on fewer resources, but the docs do not recommend it: some background processes are resource-intensive.
- Node itself is lightweight, but `Xray-core` under load can use a lot of CPU and RAM.
- Docker with the Compose plugin: the installation method is described on the requirements page in docs.rw and in the Docker documentation.

## Installation steps

1. Prepare the directory:

   ```bash
   mkdir /opt/remnawave && cd /opt/remnawave
   ```

2. Download the official `docker-compose-prod.yml` and `.env.sample` from `remnawave/backend`:

   ```bash
   curl -o docker-compose.yml https://raw.githubusercontent.com/remnawave/backend/refs/heads/main/docker-compose-prod.yml
   curl -o .env https://raw.githubusercontent.com/remnawave/backend/refs/heads/main/.env.sample
   ```

3. Generate the secrets `APP_SECRET`, `METRICS_PASS`, `WEBHOOK_SECRET_HEADER`:

   ```bash
   sed -i "s/^APP_SECRET=.*/APP_SECRET=$(openssl rand -hex 64)/" .env
   sed -i "s/^METRICS_PASS=.*/METRICS_PASS=$(openssl rand -hex 64)/" .env
   sed -i "s/^WEBHOOK_SECRET_HEADER=.*/WEBHOOK_SECRET_HEADER=$(openssl rand -hex 64)/" .env
   ```

4. Change the Postgres password (both `POSTGRES_PASSWORD` and the password inside `DATABASE_URL` change):

   ```bash
   pw=$(openssl rand -hex 24) && sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$pw/" .env && sed -i "s|^\(DATABASE_URL=\"postgresql://postgres:\)[^\@]*\(@.*\)|\1$pw\2|" .env
   ```

5. Update at least these in `.env`:
   - `FRONT_END_DOMAIN`: the panel domain, for example `panel.yourdomain.com`;
   - `SUB_PUBLIC_DOMAIN`: at first, the panel domain plus `/api/sub`, for example `panel.yourdomain.com/api/sub`.
6. Start the containers:

   ```bash
   docker compose up -d && docker compose logs -f -t
   ```

7. Right after starting, put a reverse proxy on the root path of the domain or a subdomain.

## What the installation consists of

- Containers from `docker-compose-prod.yml`: `remnawave` (Panel), `remnawave-db` (Postgres), `remnawave-redis` (Valkey).
- The Panel ports (`3000`, `3001`) and Postgres (`6767`) are bound to `127.0.0.1`; only the reverse proxy publishes them to the outside.
- Panel talks to Valkey through a Unix socket (`REDIS_SOCKET=/var/run/valkey/valkey.sock` in `.env.sample`); `REDIS_HOST` and `REDIS_PORT` are the alternative to the socket. The Environment Variables page describes `REDIS_HOST`/`REDIS_PORT` as required; if they disagree, follow `.env.sample`.
- `PANEL_DOMAIN` (optional): the panel domain for direct links, for example in Telegram notifications.
- Scaling: `API_INSTANCES` (default `1`, no more than the number of CPU cores; per the docs it may help at 40k+ users). `remnawave/backend` also has `docker-compose-advanced-prod.yml`, where the REST API and the scheduler are split into separate services; per the comments in the file, the REST API can be scaled, the scheduler cannot. There is no separate docs page for it.

## Environment variables

- The `.env` file is usually in `/opt/remnawave`.
- After changing `.env`, the containers must be recreated; a plain restart does not change the environment:

```bash
docker compose down && docker compose up -d
```

- Remnawave connects to Postgres through `DATABASE_URL` (`postgresql://{user}:{password}@{host}:{port}/{database}`); `POSTGRES_*` are used by the database container, not by Remnawave itself.
- Secrets are random strings of at least `64` characters (`openssl rand -hex 64`); `change_me` values are not acceptable in production.
- `SUB_PUBLIC_DOMAIN` sets the public subscription URL in REST API responses and in the UI. If `CUSTOM_SUB_PREFIX` is set in Subscription Page, the same path is appended to `SUB_PUBLIC_DOMAIN`.
- The full list (Telegram, webhooks, metrics, notifications, `SHORT_UUID_LENGTH`, `JWT_AUTH_LIFETIME` and others) is on the Environment Variables page in docs.rw.
- `.env.sample` has variables that are not on the docs page:
  - `SHORT_UUID_METHOD`: the format of the subscription link identifier: `nanoid` (default, length from `SHORT_UUID_LENGTH`), `uuid` or `custom` (pattern from `SHORT_UUID_CUSTOM_PATTERN`, 16–64 characters);
  - `SERVICE_SNI_VERIFICATION` (default `true`): when connecting to the Node API (`NODE_PORT`, mTLS, TLS 1.3), Panel sends an SNI derived from this Panel's CA certificate and public key (of the form `<32 hex>.<10 hex>.com`). With `false`, no SNI is sent. It pairs with the Node variable `SNI_VERIFICATION` ([nodes.md](nodes.md)): if it is enabled on the Node and disabled here, Panel will not connect to the Node.

## Reverse proxy

- Remnawave does not support publishing on a sub-path (for example, `location /remnawave {`). Only the root path of a domain or a subdomain.
- SSH Port Forwarding is not supported; only one of the reverse proxies below.
- Options in the docs: `Caddy`, `Nginx`, `Traefik`, `Angie`.
- `TryCloudflare` is for development only, not for production.

## Panel protection

The official Panel Security page describes additional layers of protection:

- `Caddy with minimal setup`;
- `Caddy with custom path`;
- `Cloudflare ZeroTrust` (per the docs: SSL Strict, Proxied, an Access application with a policy; Cloudflare-side details: skill `cloudflare`);
- `TinyAuth for Nginx`.

## Typical scenarios

- First installation of Panel on a new VPS.
- Moving an old setup to the official `docker-compose-prod.yml`.
- Fixing an insecure installation where Panel was published without a reverse proxy.

## Mistakes

- Leaving `change_me` values in secrets.
- Not changing the Postgres password.
- Trying to publish Panel on a sub-path such as `/remnawave`.
- Using SSH port forwarding as a permanent publishing setup.
- Changing `.env` and then just restarting the containers without recreating them.

## Checking the result

- `docker compose ps` shows running containers.
- `docker compose logs -f -t` shows no persistent crash-loop errors.
- Panel opens on the reverse proxy domain.
- `FRONT_END_DOMAIN` and `SUB_PUBLIC_DOMAIN` match the actual domain.
- No services are exposed directly, except the controlled reverse proxy entry point.
- After the first registration, the first user becomes `super-admin`.
