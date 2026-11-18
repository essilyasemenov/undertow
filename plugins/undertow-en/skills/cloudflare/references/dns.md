# Cloudflare DNS

The DNS side of publishing through Cloudflare: records, proxy status, DNSSEC.

## Basic rules

- The architectural difference between `Proxied` and `DNS only` is described in [SKILL.md](../SKILL.md); this section applies it to specific DNS records.
- Only `A`, `AAAA` and `CNAME` records can be proxied; records of all other types always work as `DNS only`.
- Do not describe `MX`, `TXT`, `NS`, `SRV` and most service records as proxied web traffic.
- `Proxied` is needed where traffic must go through the Cloudflare edge.
- `DNS only` is needed where Cloudflare should only return the DNS answer and not become a reverse proxy.

## How to choose a record

- `A`: the name points to the IPv4 address of the origin.
- `AAAA`: the name points to the IPv6 address of the origin.
- `CNAME`: the name points to another canonical name.
- `MX`: mail routing.
- `TXT`: domain verification, SPF/DKIM/DMARC and other text data.
- `NS`: subdomain delegation or special scenarios with authoritative servers.
- `SRV`: service lookup by name, port and priority.

## Workflow

1. Determine what is behind the name: a web resource, a mail service, a verification record or a route to a private resource.
2. Choose the record type by its function, not by habit.
3. For `A` / `AAAA` / `CNAME`, decide whether `Proxied` or `DNS only` is needed.
4. If the domain needs protection against spoofed DNS answers, check the DNSSEC scenario.
5. If the service depends on a direct IP, a non-standard transport or third-party domain verification, check separately whether `DNS only` is acceptable.

## Practical rules

- For public HTTP(S) names, consider `A`, `AAAA` or `CNAME` with `Proxied` first.
- For third-party domain verification and some SaaS integrations, do not enable proxying without explicit confirmation in the documentation.
- Describe `MX` as a mail record, not as an entry point to the Cloudflare CDN.
- Use `NS` for subdomain delegation only where a delegation boundary is really needed.
- For DNSSEC, rely on the current way the zone is connected: full setup, subdomain setup or migration.

## Checks and diagnostics

- Check the record type, name, content, TTL and proxy status separately.
- Do not mix manually created HTTPS records with proxied records on the same name without checking the official limitations.
- If in doubt whether a specific record supports `Proxied`, the official Cloudflare DNS limitations answer it (DNS section in [sources.md](sources.md)).

## What not to do

- Do not call `MX`, `TXT`, `SRV` or `NS` records "orange-clouded".
- Do not promise that any `CNAME` can be safely proxied.
- Do not invent DNSSEC steps; use only the sequence described in the documentation.
