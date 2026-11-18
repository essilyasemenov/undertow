# Troubleshooting

Diagnosing Remnawave installation and runtime problems from the official warnings and guides, without replacing source-backed analysis with guesses.

## Theory

The official materials warn in advance about several classes of problems:

- services must not be published directly to the Internet;
- a reverse proxy is mandatory;
- a sub-path is not supported;
- env changes require recreating the containers;
- `NODE_PORT` must be restricted by the firewall;
- node logs without `logrotate` can fill the disk;
- an error in the profile's Xray JSON prevents `Xray-core` from starting on the Node.

## Diagnostic order

1. Determine the failure layer:
   - install;
   - reverse proxy;
   - env;
   - node connectivity;
   - Xray startup on the Node (Config Profile);
   - subscription delivery.
2. Basic commands in the service directory (officially `/opt/remnawave` or `/opt/remnanode`; if the installation is non-standard, find the directory and container names through [discovery.md](discovery.md)):

   ```bash
   docker compose ps
   docker compose logs -f -t
   ```

3. If `.env` was changed, recreate:

   ```bash
   docker compose down && docker compose up -d
   ```

4. For the Node:
   - container logs: `docker compose logs -f -t`;
   - `Xray-core` logs: `docker exec remnanode xlogs`;
   - the Xray configuration the Node actually received from Panel: `docker exec -it remnanode cli --dump-config`;
   - the firewall for `NODE_PORT` (open only to the panel IP).
5. For subscriptions: check `SUB_PUBLIC_DOMAIN` (it matches the real public subscription URL).
6. For lost panel access: Rescue CLI.

## Checking the Xray configuration on the Node

`Xray-core` runs inside the Node container, and Panel sends the configuration. The `xray -test` command on the host does not apply here. The check per the docs: apply the profile and look at the `Xray-core` logs:

```bash
docker exec remnanode xlogs
```

## Common errors

### `XML-RPC fault: SPAWN_ERROR: xray`

The Node logs (`cd /opt/remnanode && docker compose logs -f -t`) show `SPAWN_ERROR: xray`, followed by `Failed to get system stats ... ECONNREFUSED 127.0.0.1:61000`.

- Cause: `Xray-core` did not start, most often because of a configuration error.
- Fix:
  1. Look at the `Xray-core` logs: `docker exec remnanode xlogs`; the cause is usually visible there.
  2. Fix the configuration in Panel (Config Profile) and save it.

## Useful commands

| Task | Command |
| --- | --- |
| Panel Rescue CLI | `docker exec -it remnawave cli` |
| Restart Panel | `cd /opt/remnawave && docker compose down && docker compose up -d && docker compose logs -f -t` |
| PM2 monitor in Panel | `docker exec -it remnawave pm2 monit` |
| Node Rescue CLI | `docker exec -it remnanode cli` |
| `Xray-core` logs | `docker exec remnanode xlogs` |
| Xray configuration on the Node | `docker exec -it remnanode cli --dump-config` |
| Restart Node | `cd /opt/remnanode && docker compose down && docker compose up -d && docker compose logs -f -t` |

## Rescue CLI

A built-in set of maintenance and recovery commands (`docker exec -it remnawave cli`):

- **Reset superadmin**: completely removes the superadmin; on the next browser login you will be asked to create a new one.
- **Enable password authentication**: re-enables password login if it was accidentally disabled through the OAuth settings.
- **Reset certs**: resets Remnawave's internal certificates. The docs warn not to use it without understanding the consequences.
- **Get SECRET_KEY for a Remnawave Node**: shows the `SECRET_KEY` for connecting a Node.
- **Fix Collation**: fixes database collation problems.
- **Clean up HWID Devices**: removes all saved HWID devices of users.
- **Clean up SRH Table**: clears the Subscription Request History; helps when the table has grown large and inflated the database.

The Node has its own Rescue CLI (`docker exec -it remnanode cli`) with one function, **Get cold config**: `docker exec -it remnanode cli --dump-config` prints the Xray configuration the Node received.

## Typical scenarios

- Panel does not open on its domain.
- Changes to `.env` did not apply.
- A Node was added, but Xray does not start.
- Subscription Page cannot reach Panel.
- Superadmin access was lost.

## Mistakes

- Looking for the cause in the UI when `.env` was not applied through a recreate.
- Leaving `NODE_PORT` open to the world.
- Using sub-path routing in the reverse proxy.
- Enabling logs on the node without rotation.
- Running `xray -test` on the Node host instead of looking at `xlogs`.
- Starting Rescue CLI with a command from old guides: the current command is `docker exec -it remnawave cli`.

## Checking the result

- The right failure domain has been identified.
- The fix relies on the official docs warnings and steps.
- After the fix, the service either opens or the next failure layer is clearly localized.
