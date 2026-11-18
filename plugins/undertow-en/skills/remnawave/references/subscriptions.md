# Subscriptions: Hosts, Templates, Response Rules, Subscription Page

The subscription delivery chain: Subscription URL, Hosts, Templates, `Subscription` → `Settings`, Response Rules, External Squads and Subscription Page.

## Delivery chain

1. The user receives a Subscription URL.
2. A browser or client app requests this URL; Remnawave itself determines who is asking: it returns a web page to a browser and a configuration in a suitable format to a client.
3. `Hosts` define the entry points (address, port, linked inbound).
4. `Templates` define the configuration format for a family of clients.
5. `Response Rules` choose which response and Template a specific request gets.
6. `Subscription` → `Settings` adds metadata for supported clients (for example, `Subscription Name`).
7. `External Squads` override Templates and settings for groups of users.
8. Subscription Page hides the panel domain from end users.

Response Rules and Templates belong to subscription delivery. They are not `Server-Side Routing` on Nodes ([config-profiles.md](config-profiles.md)) and not Happ Routing ([happ-routing.md](happ-routing.md)).

## Hosts

- A Host is an entry point through which the user reaches Nodes. The client receives the list of Hosts and picks one (for example, a "Finland" Host with only Finnish Nodes).
- `Hosts` → `Create new host`:
  - `Host visibility`: whether to show the Host in the subscription; clients do not see a disabled Host;
  - `Remark`: the name in the dashboard;
  - inbound: **exactly one** per Host, chosen from any Config Profile; the port is taken from the inbound (it may differ in advanced configurations);
  - `Address`: an IP or domain that points to the IP of the needed Node.
- The docs advise a domain instead of an IP: when the IP changes, updating DNS is enough, and users do not need to refresh the subscription.
- `Advanced Options` override inbound parameters (for example, `SNI` instead of `serverNames`); empty fields are taken from the inbound. The docs advise not to touch them unless necessary.

## Templates

Format families:

| Family | For which clients |
| --- | --- |
| `Mihomo` | clients on the Mihomo core (Clash's successor); there are special Remnawave keys for Mihomo |
| `Xray-json` | clients on the Xray core |
| `Sing-box` | clients on the Sing-box core |
| `Base64` | a list of configurations in Base64; there is no Template, it is used as a fallback if the client did not match the other formats |

- Since version 2.2.0 you can create several Templates for each family and hand them out through External Squads or Response Rules.
- `XRAY_JSON` has the `injectHosts` directive (since 2.6.3): Panel inserts the outbounds of the selected Hosts into the Template (balancers, complex routing). Conditions: the virtual Host is enabled and not hidden; the injected Hosts are enabled (hidden ones are taken by default); the inbound of every Host is in the user's Squad. Details are in the "Xray JSON Advanced" article in the docs.
- The docs do not provide a universal matrix of which client gets which Template by User-Agent.

## Response Rules (SRR)

An ordered JSON set of rules that the backend checks for each subscription request from top to bottom; the first matching rule stops the check. Response Rules override External Squads settings.

Rule fields:

| Field | Value |
| --- | --- |
| `name` | required, 1–50 characters |
| `description` | up to 250 characters |
| `enabled` | required; `false` means the rule is skipped |
| `operator` | `AND` (all conditions) or `OR` (any) |
| `conditions` | list of conditions; empty matches everything (for a fallback) |
| `responseType` | `MIHOMO`, `CLASH`, `STASH`, `SINGBOX`, `XRAY_JSON`, `XRAY_BASE64`, `BROWSER`, `BLOCK` (403), `STATUS_CODE_404`, `STATUS_CODE_451`, `SOCKET_DROP` |
| `responseModifications` | `subscriptionTemplate`, `headers` (`key`/`value`), `applyHeadersToEnd`, `ignoreHostXrayJsonTemplate`, `ignoreServeJsonAtBaseSubscription`, `disableHwidCheck` |

A condition: `headerName` (per RFC 7230, the name is case-insensitive), `operator` (`EQUALS`, `NOT_EQUALS`, `CONTAINS`, `NOT_CONTAINS`, `STARTS_WITH`, `NOT_STARTS_WITH`, `ENDS_WITH`, `NOT_ENDS_WITH`, `REGEX`, `NOT_REGEX`), `value` (1–255 characters), `caseSensitive`. Multiple header values are joined with a comma; if the header is missing, the rule is skipped.

Example from the docs: Happ on Android gets its own Template.

```json
{
  "name": "Happ Android",
  "enabled": true,
  "operator": "AND",
  "conditions": [
    { "caseSensitive": false, "headerName": "user-agent", "operator": "CONTAINS", "value": "happ" },
    { "caseSensitive": false, "headerName": "x-device-os", "operator": "CONTAINS", "value": "android" }
  ],
  "responseType": "XRAY_JSON",
  "responseModifications": { "subscriptionTemplate": "Happ Android" }
}
```

The docs warn that incorrect changes to Response Rules can break the system.

## Subscription Page

A separate container that hides the panel domain from users. Options: `Bundled` (on the panel server) and `Separate server`.

1. In the panel's `.env`, change `SUB_PUBLIC_DOMAIN` to the subscription page domain (without `http`/`https`) and recreate the panel containers.
2. Create an API Token in `Remnawave Settings` → `API Tokens`.
3. In the Subscription Page `.env` (officially `/opt/remnawave/subscription`):
   - `APP_PORT=3010` (the container is published on `127.0.0.1:3010`);
   - `REMNAWAVE_PANEL_URL`: `http://remnawave:3000` for Bundled or the public panel domain for Separate server;
   - `REMNAWAVE_API_TOKEN`: the token you created;
   - `CUSTOM_SUB_PREFIX`: a custom path (append the same path to `SUB_PUBLIC_DOMAIN`);
   - `TRUST_PROXY`: how many proxies in front of the app to trust when reading `X-Forwarded-For`; `1` for one reverse proxy on the same host, more if there are other proxies in front (for example, Cloudflare → Nginx → app).
4. `docker compose up -d && docker compose logs -f`, then a reverse proxy on the root path of the domain (a sub-path is not supported). In an existing Caddyfile, add a new block instead of replacing the whole config.
5. The page is available at `https://<domain>/<shortUuid>`.

The look and the list of apps are configured in `Subpage Builder` in the dashboard. The `Show Connection Keys` toggle shows raw keys; it has no effect when HWID is enabled; after changing it, the page container must be restarted.

## Mistakes

- Treating a Host as a container for several inbounds: a Host has only one inbound.
- Confusing Templates and Hosts: a Host is an entry point, a Template is a format.
- Confusing Response Rules with `Server-Side Routing` or Happ Routing.
- Not recreating the panel containers after changing `SUB_PUBLIC_DOMAIN`.
- Starting Subscription Page without `REMNAWAVE_API_TOKEN`.
- Publishing Subscription Page on a sub-path instead of using `CUSTOM_SUB_PREFIX`.
- Leaving `TRUST_PROXY=1` when Cloudflare also sits in front of the reverse proxy.

## Checking the result

- A browser opening the Subscription URL gets a web page; a client opening the same URL imports the configuration.
- The user sees only Hosts with `Host visibility` enabled.
- Subscription Page serves data on the expected public domain.
- External Squads and Response Rules overrides are visible in the delivered subscription.
