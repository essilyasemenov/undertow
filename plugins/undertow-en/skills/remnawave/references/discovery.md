# Discovering the actual installation

Paths, container names and file names in the other references come from the official installation: `/opt/remnawave`, `/opt/remnanode`, `/opt/remnawave/subscription`, containers `remnawave` and `remnanode`. On a real server the installation may differ: another directory, renamed containers, a custom compose file, a separate reverse proxy, custom scripts.

So before commands that depend on a path or container name, first find out the actual location, unless the user has confirmed that the installation is official. Then substitute the values you found into the commands.

All commands below only read and change nothing. The user runs them on their own server. If Claude Code is running on another machine, do not search the local disk: there are no Remnawave files there, and the home directory holds data unrelated to the task.

## Containers and images

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
```

The `Image` column shows which container is Panel (`remnawave/backend`), Node (`remnawave/node`), Subscription Page, database and cache, and which tag they have. Use the name from the `Names` column in `docker exec <name> ...` instead of `remnawave` and `remnanode`.

## Where the compose files are

All compose projects on the server and the paths to their files:

```bash
docker compose ls
```

The directory and compose file of a specific container:

```bash
docker inspect <container_name> --format '{{ index .Config.Labels "com.docker.compose.project.working_dir" }}'
docker inspect <container_name> --format '{{ index .Config.Labels "com.docker.compose.project.config_files" }}'
```

Use the directory you found instead of `/opt/remnawave` or `/opt/remnanode`. If there are no labels, the container was not started through Docker Compose, and `docker compose ...` commands do not apply to it.

## Environment variables

Variable names only, without values: the values contain secrets.

```bash
docker inspect <container_name> --format '{{range .Config.Env}}{{println .}}{{end}}' | cut -d= -f1 | sort
```

The value of a specific non-secret variable (for example, `SUB_PUBLIC_DOMAIN`, `FRONT_END_DOMAIN`):

```bash
docker inspect <container_name> --format '{{range .Config.Env}}{{println .}}{{end}}' | grep '^SUB_PUBLIC_DOMAIN='
```

Do not ask the user to send the whole `.env` or output containing `APP_SECRET`, passwords, `SECRET_KEY` or tokens.

## Ports and reverse proxy

```bash
ss -lntp
```

Shows who listens on `80`/`443` (the reverse proxy), the Panel ports (by default `127.0.0.1:3000`) and `NODE_PORT` on the Node. If the reverse proxy also runs in a container, it is visible in `docker ps`.

## Installations without Docker or with custom scripts

```bash
systemctl list-units --type=service | grep -iE 'remna|xray|caddy|nginx'
```

```bash
find / -xdev \( -name '*compose*.y*ml' -o -name '.env' \) -path '*remna*' 2>/dev/null
```

If the installation is non-standard, give the commands from the other references as a template and say explicitly that they assume the official installation.

## What to do with the result

- It matches the official installation: use the other references as is.
- It differs: substitute the actual directories and container names; about the differences (custom compose, another reverse proxy), say that docs.rw does not describe them.
- Do not change the user's files or restart services until they have confirmed the plan.
