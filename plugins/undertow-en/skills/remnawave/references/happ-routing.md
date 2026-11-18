# Happ Routing

What is officially known about Happ Routing in Remnawave and where its limits are.

## What is confirmed

- The panel's `Utilities` menu section contains `Happ Routing`, a builder for creating and managing routing rules for the Happ client.
- A user's `Detailed Info` contains Happ Crypto links ([users.md](users.md)).
- docs.rw has no separate step-by-step page with all Happ Routing fields, the export format and example rules.

## What Happ Routing is not

| Mechanism | Where it applies |
| --- | --- |
| Happ Routing | routing rules for the Happ client |
| Server-Side Routing | routing traffic on the Node through a Config Profile ([config-profiles.md](config-profiles.md)) |
| Response Rules | which response and Template a subscription request gets ([subscriptions.md](subscriptions.md)) |

## Practice

1. Make sure the task is about Happ Routing, not Server-Side Routing, Templates or Response Rules.
2. In the panel, open `Utilities` → `Happ Routing`.
3. If the exact field schema, export format or internal rule logic is needed, say directly that docs.rw does not describe it, and rely on the current panel interface.

## Mistakes

- Attributing `Server-Side Routing` steps to Happ Routing.
- Inventing an undocumented rule schema.
- Assuming docs.rw contains a full description of the Happ Routing fields.
