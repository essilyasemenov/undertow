# Nodes

Deploying and connecting a Remnawave Node, the node firewall, assigning a Config Profile, the operational card, officially described advanced practices and Node Plugins.

## Theory

The official documentation defines `Remnawave Node` as a lightweight container that includes `Xray-core`. Panel does not include `Xray-core`, so running Remnawave in practice requires a Node.

The `Nodes` guide explicitly warns that it does not cover installation: installation steps come from the `Remnawave Node` page, and the UI interpretation from the learning materials. Do not mix installation and dashboard semantics.

## Installing a Node

1. Make sure Docker with the Compose plugin is installed on the node server.
2. Create the directory:

   ```bash
   mkdir /opt/remnanode && cd /opt/remnanode
   ```

3. In Panel, open `Nodes` → `Management` and click `+`.
4. Fill in the form. `Node Port` is the port on which the Node accepts internal API requests from Panel; it is not used for anything else.
5. Click `Copy docker-compose.yml`.
6. Create `docker-compose.yml` on the node server and paste the content:

   ```bash
   cd /opt/remnanode && nano docker-compose.yml
   ```

7. Start it:

   ```bash
   docker compose up -d && docker compose logs -f -t
   ```

8. Return to Panel, click `Next`, select a `Config Profile` and click `Create`.
9. Close `NODE_PORT` with a firewall rule, allowing it only for the panel IP.

In the copied `docker-compose.yml`, the Node runs with `network_mode: host`, and `NODE_PORT` and `SECRET_KEY` are passed through `environment`. `SECRET_KEY` can also be obtained through the panel's Rescue CLI ([troubleshooting.md](troubleshooting.md)).

### SNI verification on `NODE_PORT`

The Node variable `SNI_VERIFICATION` (default `false`, set in `environment` in the Node's `docker-compose.yml`):

- with `true`, the Node accepts a TLS handshake on `NODE_PORT` only with an SNI derived from the Panel's CA certificate and public key in `SECRET_KEY`; with another SNI or none, the connection is dropped before the Node certificate is sent (`unknown sni`). A scanner that does not know this SNI does not see the Node API certificate;
- the Node prints the expected SNI in its log at startup, in the `SECRET_KEY OK` block;
- Panel sends this SNI only if it has `SERVICE_SNI_VERIFICATION=true` (the default, [install.md](install.md)). Do not enable `SNI_VERIFICATION` on the Node while verification is disabled on the Panel: Panel will not connect.

docs.rw does not describe these variables; the behavior was established from the source code of `remnawave/backend` 3.4.11 and `remnawave/node` 3.4.6.

## Operational card

The `Nodes` guide describes:

- `Node Vitals`: Country, Internal name, Address (Node IP or domain), Port;
- `Consumption`: the multiplier for counting user traffic (`1.0` is normal counting, `0.5` and `2.0` change the billing equivalent);
- `Core Configuration`: choosing the `Config Profile`. One Node gets **only one** Profile, since a profile is a complete `Xray-core` configuration; several `Inbounds` can be activated within the profile;
- `Tracking & Billing`: `Infrastructure Provider`, `Track traffic usage`, `Traffic limit`, `Reset day`, `Notification %`. Panel always records traffic; the checkbox enables control against the limit;
- `Node Management` and status indicators: number of connections (duplicates are counted), `Xray-core` version, Remnawave Node version;
- the `Actions` block: `Update`, `Restart all nodes`;
- `More actions`: `Show usage`, `Copy Node UUID`, `Disable`, `Delete`.

## Advanced usage

### Custom geosite and geoip

- Additional files are mounted into `/usr/local/share/xray/` inside the container, **each file separately**. Mounting the whole folder overwrites the standard geosite/geoip files.
- In the Xray config the file is referenced as `ext:<file>.dat:<category>`.
- Routing on the Node controls server traffic and does not affect client `DIRECT` connections; client-side routing is configured on the client.

### Node logs on the host

- Mount `/var/log/remnanode` into the container and set the paths in the `log` section of the Xray config (`error.log`, `access.log`).
- Be sure to configure `logrotate`, otherwise the logs will fill the disk:

```bash
mkdir -p /var/log/remnanode
sudo apt update && sudo apt install logrotate
nano /etc/logrotate.d/remnanode
logrotate -vf /etc/logrotate.d/remnanode
```

Example configuration from the docs: `size 50M`, `rotate 5`, `compress`, `missingok`, `notifempty`, `copytruncate`.

### TLS certificates for Xray

- Needed for a TLS transport (for example, `VLESS-Vision-TLS`); not needed for Reality.
- Certificates are mounted **into the Panel container** in the directory `/var/lib/remnawave/configs/xray/ssl/`. When sending the configuration, Panel reads the files itself and passes the certificates to the Node.
- In the Xray config, refer to the internal path, for example `/var/lib/remnawave/configs/xray/ssl/privkey.key` and `fullchain.pem`; watch the `.key` and `.pem` extensions.

## Node Plugins (β)

Additional modules on the Node: **Torrent Blocker**, **Ingress Filter**, **Egress Filter**, the **Connection Drop** setting, and **Shared Lists**. Available since Panel and Node `v2.7.0`. There are also **Pre Start** (Cleanup Sockets: removes the listed socket files when Xray starts, requires Node `v3.0.0`) and **Executor** (commands: temporarily block and unblock an IP, reset the `nftables` table; plugins are not required, but `NET_ADMIN` is).

Requirements:

- the `cap_add: NET_ADMIN` directive in the Node's `docker-compose.yml`;
- `nftables` on the host (`nft --version`);
- Linux kernel `5.7` or later (`uname -r`).

The Torrent Blocker, Ingress Filter and Egress Filter plugins work directly with the server firewall: the Node creates the table `ip remnanode` in `nftables`.

| Plugin | What it does | Important |
| --- | --- | --- |
| Torrent Blocker | Blocks for `blockDuration` seconds the IP from which torrent traffic was detected; adds its rule first in `routing.rules` | Requires `Xray-core` ≥ `26.3.27` and `sniffing` with `destOverride` (`http`, `tls`, `quic`) on the inbound |
| Ingress Filter | Permanently blocks incoming traffic from the listed IPs/CIDRs | The docs call it a very dangerous tool |
| Egress Filter | Blocks outgoing connections to IPs/CIDRs and ports (for example, 25, 465, 587) | — |
| Connection Drop | IP whitelist for automatically dropping connections when a user is deleted | Dropping always works with `NET_ADMIN` (since Node `v2.6.0`); the whitelist is needed, for example, for bridges |
| Shared Lists | Named IP lists for other plugins | Format `ext:<name>`, type `ipList` |

Each plugin has its own fields; all have `enabled` (disabled by default):

| Plugin | Fields |
| --- | --- |
| `torrentBlocker` | `ignoreLists.ip` (no CIDR), `ignoreLists.userId`, `blockDuration` (seconds), `includeRuleTags` (optional: also block by your own rules with `ruleTag`) |
| `ingressFilter` | `blockedIps` (IP/CIDR, IPv4/IPv6) |
| `egressFilter` | `blockedIps`, `blockedPorts` |
| `connectionDrop` | `whitelistIps` |
| `sharedLists` | `name`, `type`, `items` |

The docs text does not describe where exactly in the Panel UI the plugin configuration is edited (it is shown only in a screenshot).

## Typical scenarios

- Connecting the first Node to Panel.
- Assigning a new Config Profile to a Node.
- Setting the traffic coefficient for billing semantics.
- Enabling node-side limit tracking with a monthly reset.
- Mounting geosite/geoip files into a Node.
- Moving node logs to the host filesystem with `logrotate`.
- Passing TLS certificate files to a Node through Panel.
- Blocking torrents or unwanted outgoing ports with Node Plugins.

## Mistakes

- Opening `NODE_PORT` to the Internet.
- Mounting the whole `/usr/local/share/xray/` directory, overwriting the default geosite/geoip files.
- Enabling logs without log rotation.
- Assuming that server-side routing affects client `DIRECT` connections.
- Mounting TLS certificates into the Node container instead of Panel.
- Enabling Torrent Blocker without `sniffing` on the inbound.
- Enabling plugins without `cap_add: NET_ADMIN`.
- Ignoring the `Consumption` multiplier and misreading the actual user traffic usage.

## Checking the result

- The Node shows up in `Nodes` → `Management`.
- The needed `Config Profile` is selected for the Node.
- `docker compose logs -f -t` on the node server shows no persistent errors.
- `NODE_PORT` is reachable only from the Panel IP.
- `Consumption` and `Tracking & Billing` are configured if needed.
- For plugins: the `remnanode` table is visible in `nft list ruleset`.
