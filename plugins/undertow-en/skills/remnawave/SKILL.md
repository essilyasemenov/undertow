---
name: remnawave
description: "Remnawave 3.x (proxy management panel on top of Xray-core): installing Panel and Node, docker compose, .env (APP_SECRET, FRONT_END_DOMAIN, SUB_PUBLIC_DOMAIN, PANEL_DOMAIN), Valkey/Redis, reverse proxy (Caddy, Nginx, Traefik, Angie), panel protection, upgrading, Nodes, NODE_PORT, SECRET_KEY, Node Plugins (Torrent Blocker, Ingress/Egress Filter, Connection Drop, Shared Lists), Config Profiles, Xray JSON, inbounds, snippets, Internal Squads, Hosts, server-side routing and cascade (bridge) between Nodes, troubleshooting (SPAWN_ERROR, xlogs, Rescue CLI), Users, Internal and External Squads, HWID device limit, subscriptions (Subscription URL, Hosts, Templates Mihomo/Xray-json/Sing-box/Base64, Response Rules, Subscription Page, injectHosts), REST API and API Tokens with scopes, Happ Routing, finding the actual installation files on the server (where .env, docker-compose.yml and configs live, panel and node containers, non-standard installation). Use for any task about Remnawave Panel and Node, based only on docs.rw and github.com/remnawave."
license: MIT
---
# remnawave

The common entry point for Remnawave tasks. Answer in English.

Remnawave is a proxy management tool on top of `Xray-core`. Components per the official documentation: Panel (the main entry point), Backend (NestJS), Frontend (React), Node (a lightweight container with `Xray-core`), XTLS-SDK, XTLS-SDK-NestJS. Panel does not contain `Xray-core`, so at least one Node is needed for it to work.

Installation chain from the quick start: Remnawave Panel → Reverse Proxy → Subscription Page (optional) → Remnawave Node.

## How to work with this skill

1. Determine the area of the task: installation, upgrade, Nodes, Config Profiles, users, subscriptions, API, Happ Routing or diagnostics.
   - A new installation and an upgrade are different operations. If the question does not imply that Remnawave is already running, treat it as a new installation and do not mention old versions, migration or deprecated variables.
   - Upgrade only when the user says so or an existing installation is visible. First find out which version they are upgrading from and to: an upgrade within 3.x and the move from 2.x to 3.x are different scenarios ([upgrade.md](references/upgrade.md)).
2. Pin down the version-sensitive context:
   - which Panel and Node release is used;
   - where Panel and Node are hosted;
   - whether there is a reverse proxy;
   - whether a UI workflow or a REST API workflow is needed.
3. Panel and Node run on the user's servers. If Claude Code is not running on that server (usually it is not), do not search for Remnawave files on the local disk and do not read the user's home directory: give commands the user will run on the server.
4. Paths and container names in the references come from the official installation (`/opt/remnawave`, `/opt/remnanode`, containers `remnawave`, `remnanode`). If the work concerns an existing server and the user has not confirmed that the installation is official, first offer the discovery commands from [discovery.md](references/discovery.md) and substitute the actual directories and names.
5. Open the relevant section and do not invent unconfirmed features, parameters or UI steps.
6. Do not make a production change until the step is confirmed by the official documentation.

## Sections (`references/`)

| Task | File |
| --- | --- |
| Existing server: where the compose files and `.env` actually are, which containers and ports | [discovery.md](references/discovery.md) |
| New installation: requirements, Panel, `.env`, reverse proxy, panel protection | [install.md](references/install.md) |
| Upgrading and moving from 2.x to 3.x | [upgrade.md](references/upgrade.md) |
| Node installation, firewall, operational card, geo files, logs, TLS certificates, Node Plugins | [nodes.md](references/nodes.md) |
| Config Profiles, inbound activation chain, snippets, server-side routing and cascade | [config-profiles.md](references/config-profiles.md) |
| Users, Internal and External Squads, Bulk Actions, HWID device limit | [users.md](references/users.md) |
| Subscription: Hosts, Templates, Response Rules, Subscription Page | [subscriptions.md](references/subscriptions.md) |
| REST API, API Tokens and scopes, built-in documentation | [api.md](references/api.md) |
| Happ Routing and its limits | [happ-routing.md](references/happ-routing.md) |
| Diagnostics: failure layers, Xray logs, common errors, Rescue CLI | [troubleshooting.md](references/troubleshooting.md) |
| Official links | [sources.md](references/sources.md) |

## Working order

```text
remnawave task
  -> classify scope
    -> confirm official source
      -> choose reference
        -> check version-sensitive behavior
          -> apply only documented workflow
```

## Quality rules

- Sources of facts: only `docs.rw` and `github.com/remnawave`. Syntax and behavior of Xray itself: the official Xray documentation (`xtls.github.io`).
- If a feature, endpoint, UI element or operational behavior is not confirmed, say explicitly that it is not confirmed.
- Do not mix installation, API and subscription setup into one unchecked answer.
- For production-critical tasks, take into account the reverse proxy, which services are exposed, and version-specific behavior.
- The material was checked against Remnawave backend `3.4.11` (details in [sources.md](references/sources.md)). The changelog describes changes in newer releases.
- Do not confuse Happ Routing with Server-Side Routing: the official materials distinguish them.

## Related skills

- DNS, routing, MTU, reverse proxy, firewall, TLS, Linux networking: skill `network`.
- Publishing Panel, subscriptions and Node through Cloudflare: skill `cloudflare`.
- Choosing a topology (direct, cascade, CDN, WARP): skill `architecture`.
- Before the final decision on Nodes, Hosts and routing, run skill `detection-audit`.
