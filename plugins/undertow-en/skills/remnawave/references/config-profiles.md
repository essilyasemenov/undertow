# Config Profiles

Creating Config Profiles, working with Inbounds, the chain that activates a profile on Node, Host and Squad, snippets and server-side routing (a cascade between Nodes).

## Theory

The official documentation defines a `Config Profile` as a complete `Xray-core` configuration template for a Node. The profile contains all the Inbounds and shared settings the Node needs.

The docs also warn that:

- Remnawave articles do not teach how to configure `Xray-core` itself;
- Xray syntax and behavior are described in the official Xray documentation (`xtls.github.io/config`).

Remnawave deliberately clears the `clients` array in the Node configuration: the Panel itself fills users into the inbound. This is not a bug.

## Creating a profile

1. Open `Config Profiles` and click `Create Config Profile`.
2. Enter the profile name.
3. In the editor that opens:
   - add or remove `Inbounds`;
   - adjust the other Xray settings.
4. If needed, use `Load from GitHub` for a template.
5. Save the profile and return to the list. Under the profile name, the left icon shows the number of `Inbounds`, the right one the number of `Nodes` using the profile.

## Activation chain

For a new inbound to actually reach the user, the docs describe this sequence:

1. Create or change a `Config Profile`.
2. Assign the profile to a Node: `Nodes` → `Management` → Node card → `Change Profile`.
3. Enable the needed `Inbounds` on this Node.
4. On `Hosts`, assign a specific inbound from the profile.
5. In `Internal Squads` (for example, `Default-Squad`), enable this inbound.

If the last step is skipped, the user will not get access to the new inbound even with correct Node and Host settings.

## Snippets

- A snippet is a predefined array of `"outbounds"` or `"routing"` (rules) objects that is applied in all profiles. Handy when many profiles share the same rules.
- The snippets menu opens with the `{ }` button at the bottom of the editor → `+ New snippet`. The content must be in square brackets `[]`.
- In Xray JSON a snippet is included with the object `{ "snippet": "<name>" }`, for example inside `routing.rules`.

## Server-side routing (cascade, bridge)

The docs show a demonstration (not production-ready) setup with two Nodes, `RU` and `DE`: users connect to `RU`, traffic to `.ru` exits directly from `RU`, and everything else goes through `DE`. The docs call this setup a bridge.

1. **Profile for DE.** A separate Config Profile (for example, `DE Bridge Profile`) with an inbound for the bridge (in the example `shadowsocks`, tag `BRIDGE_DE_IN`, port `9999`, `network: tcp,udp`, sniffing enabled) and outbounds `DIRECT` (`freedom`), `BLOCK` (`blackhole`). Assign the profile to Node `DE` and select `BRIDGE_DE_IN`.
2. **Internal Squad for the bridge.** Create, for example, `Bridge Squad` and enable `BRIDGE_DE_IN` in it.
3. **Service user.** Create a user (for example, `bridge_user`) with `Data Limit` = `0` and an `Expiry Date` far in the future, and assign `Bridge Squad` to it. Take the password from the user card: `More Actions` → `Detailed Info` → `Connection Information` (Trojan Password, VLESS UUID or SS Password, depending on the inbound protocol).
4. **Public RU profile.** In the profile users connect to, add an outbound to DE (in the example `SS_OUTBOUND_TO_DE`: the DE Node address, the `BRIDGE_DE_IN` port, the service user's password; for Shadowsocks in Remnawave the method is always `chacha20-ietf-poly1305`) and routing rules.

Xray processes rules from top to bottom. The order from the example:

1. `geoip:private` → `BLOCK`;
2. `geosite:private` → `BLOCK`;
3. `bittorrent` → `BLOCK`;
4. `geoip:ru` → `DIRECT` (the RU Node is the exit point);
5. `geosite:category-ru` → `DIRECT`;
6. everything else from `PUBLIC_RU_INBOUND` → `SS_OUTBOUND_TO_DE`.

Instead of Shadowsocks, VLESS can be used for the transit hop, with the configuration updated accordingly. Choosing between such a cascade, an L4 relay and a CDN: skill `architecture`.

## Typical scenarios

- Create the profile `Sample` and add a second `VLESS` inbound.
- Activate a new profile on an existing Node.
- Extend user access to new inbounds through `Default-Squad`.
- Move shared routing rules into a snippet.
- Build an RU → DE cascade with direct exit for Russian resources.

## Mistakes

- Treating a Config Profile as self-sufficient without assigning it to a Node.
- Trying to assign several profiles to one Node: only one is allowed.
- Assigning an inbound to a Host but forgetting to enable it in the `Internal Squad`.
- Writing users into `clients` by hand: Remnawave clears this array.
- Putting the fallback rule above specific rules: Xray checks rules from top to bottom.
- Limiting the service user by traffic or expiry: the bridge will stop working.
- Using the Remnawave guide as a replacement for the full `Xray-core` documentation.

## Checking the result

- The new profile appears in the `Config Profiles` list.
- The profile shows the correct number of `Inbounds` and `Nodes`.
- The needed profile is active on the Node.
- The needed inbound is available on the Host.
- The inbound is also enabled in the `Internal Squad`.
- The profile applied without Xray startup errors: `docker exec remnanode xlogs` on the Node ([troubleshooting.md](troubleshooting.md)).
