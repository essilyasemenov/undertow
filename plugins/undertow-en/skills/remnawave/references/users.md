# Users and Squads

Creating and maintaining Users, limits, subscription expiry, Internal and External Squads, HWID device limit.

## Theory

A Remnawave user gets a Subscription URL and a set of limits:

- `Data limit`: the traffic quota in GB;
- `Traffic reset strategy`: how often the counter is reset;
- the subscription expiry date;
- one or more `Internal Squads` (what is available);
- optionally an `External Squad` (what is delivered in the subscription and how).

The first registered panel user becomes `super-admin`. A forgotten password is recovered through Rescue CLI ([troubleshooting.md](troubleshooting.md)).

## Creating a user

1. `Users` → `Create user`.
2. Username: anything, but without spaces.
3. `Traffic & Limits`: `Data limit`, `Traffic reset strategy`.
4. `Access Settings`: subscription expiry date, one or more `Internal Squads`, optionally an `External Squad`.
5. `Create user`.

The Subscription URL is copied with the link icon in the list or taken from `Edit user`. Opened in a browser, it shows the Subscription Page.

## User tools

`Edit user` (pencil icon) → `More actions`:

| Item | What it shows |
| --- | --- |
| `Detailed Info` | additional data, including the VLESS UUID and Happ Crypto links |
| `Show usage` | detailed traffic statistics |
| `HWIDs and Devices` | devices reported by client apps (not all clients support this) |
| `Subscription QR Code` | a QR code of the Subscription URL |
| `Subscription links` | raw `vless://`, `ss://` and similar links |
| `Request History` | subscription requests made by client apps |

The `Tools` section also has `HWID Inspector` (HWIDs from clients) and `SRH Inspector` (analysis of subscription requests).

## Bulk Actions

The red gear button on the right of the `Users` page. Applies to all users or to the selected ones (checkboxes, filters): enable/disable, a single limit and reset strategy, extending the subscription and more.

## Internal Squads

- An Internal Squad is an access group: which Inbounds its members can use. Inbounds can be chosen from any Config Profiles.
- A user can be in several Internal Squads (for example, "regular" and "premium").
- Creating: `Internal Squads` → `+`, or `Edit` on an existing one.
- The arrow next to `Edit`: `Add users` (add everyone), `Remove users` (remove everyone), `View accessible nodes` (which Nodes the members can use).

## External Squads

- Since version 2.2.0. They override what users get in the subscription: Templates and settings from `Subscription` → `Settings` (for example, `Announce`).
- Example from the docs: separate External Squads for different countries with their own Templates.
- Creating: `External Squads` → `+`; tabs `Templates` and `Settings`.
- Response Rules take priority over External Squads ([subscriptions.md](subscriptions.md)).

## HWID device limit

- Limits the number of devices that can add the subscription. Optional, disabled by default.
- Setting: `Subscription` → `Settings` → `HWID Device Limit`; it can be overridden for an External Squad.
- The default (fallback) limit is set in the same place, `Subscription` → `Settings` → `HWID Device Limit` (in the API, `hwidSettings.fallbackDeviceLimit`); there is also `maxDevicesAnnounce`, the message shown to the user when the limit is reached. The docs page calls it `HWID_FALLBACK_DEVICE_LIMIT`, but in 3.4.11 there is no such environment variable: do not put it in `.env`.
- Per user: an individual limit (otherwise the fallback applies) or disabling the limit.
- Works only with clients that send the HWID header. If the limit is enabled and the client does not send the header, Remnawave answers `404` and the subscription cannot be fetched until the limit is disabled for that user.
- Clients with support per the docs: Happ, v2RayTun, community forks (Koala Clash, FlClashX, Prizrak-Box), Incy, RenoarX, DeskBox, Passwall; in Throne, Shadowrocket, Clash Mi and Karing support is disabled by default.
- Headers: `x-hwid`, `x-device-os`, `x-ver-os`, `x-device-model`. Since Panel 3.0.0, `x-hwid` must match `^[a-zA-Z0-9=-]{10,64}$`, otherwise it is ignored.
- Subscription response headers show why a client was refused:
  - `x-hwid-active: true`: the HWID device limit is enabled in the panel;
  - `x-hwid-not-supported: true`: the limit is enabled, but the client did not send `x-hwid`;
  - `x-hwid-max-devices-reached: true`: the user has reached the device limit;
  - `x-hwid-limit: true`: the same when the limit is reached, for backward compatibility with v2RayTun.
- Rescue CLI can delete all saved HWID devices.

## Mistakes

- Using spaces in the username.
- Creating a user without the needed `Internal Squad`: access to Inbounds will be incomplete.
- Enabling the HWID device limit without checking users' clients: clients without HWID will get `404`.
- Putting `HWID_FALLBACK_DEVICE_LIMIT` into `.env`: in 3.x the limit is configured in the panel.
- Expecting an External Squad to override a Response Rule: Response Rules take priority.
- Treating `Detailed Info` or `HWIDs and Devices` as a source of fields that are not in the docs.

## Checking the result

- The user is visible in the `Users` list, and the `Total`, `Active`, `Expired` statuses are correct.
- The Subscription URL opens in a browser.
- After importing the subscription, the client connects to the Node.
