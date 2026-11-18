---
name: architecture
description: "Censorship-resistant network architecture: diagnosing restricted or throttled access (DNS, IP blocking, SNI/TLS filtering, protocol fingerprinting, TCP shaping, UDP/QUIC blocking), choosing a topology: direct, cascade (through an intermediate VPS), CDN, selective Cloudflare WARP, relay on iptables or HAProxy, Xray-core, VLESS, Reality, XHTTP, WebSocket, gRPC on Remnawave Nodes. Use when you need to choose or revisit a censorship-circumvention setup, understand at which layer traffic is cut, how an ISP's DPI or TSPU (Russia's state-mandated DPI) recognizes and blocks VLESS, Reality, XHTTP and other protocols (active probing, TLS fingerprint, SNI, connection freezing, whitelists), plan a cascade or a fallback path, prepare a verification and rollback runbook. Also safely changing the firewall (iptables, nftables, ufw) and routes on a VPS, Node or intermediate cascade server without losing SSH access: rule backup, a second session, the provider console, rollback."
license: MIT
---
# architecture

Build the smallest topology that satisfies the observed restrictions of the user's network. Product versions, installation commands, provider behavior, blocking methods and client compatibility change over time. Answer in English.

## Main process

1. Pin down the environment:
   - Client OS and app, or router model.
   - Access network: fixed, mobile or both.
   - VPS location, OS, public IPs, domains and administrative access.
   - Required behavior: full tunnel, selected domains, selected devices, failover or exit in a specific region.
   - Current symptoms and tests already done.

2. Diagnose before choosing a topology:
   - Distinguish DNS failure, IP blocking, SNI/TLS filtering, protocol fingerprinting, TCP shaping, UDP/QUIC blocking and geographic restrictions on the service side.
   - Compare direct access, access by IP, encrypted DNS, TCP versus UDP, and the same endpoint from another provider.
   - Keep exact commands, times, client versions and error messages.

3. Choose the minimal sufficient architecture:
   - A direct foreign VPS is the simplest baseline.
   - A local or intermediate VPS plus a foreign VPS, when foreign destinations are throttled or unreachable.
   - Selective WARP egress only for destinations that reject or misclassify the VPS address.
   - A router-based setup, when several or managed devices need transparent routing.
   - A path through a CDN, when a domain, valid TLS and a reachable CDN edge give a useful alternative route.
   - Keep a documented fallback path, such as a tunnel over SSH, when practical.

4. Current facts before commands:
   - Version numbers, package repositories, certificate behavior, UI names and protocol defaults in the reference may become outdated; the source of truth is the official release pages and documentation of Xray-core, Remnawave, Cloudflare WARP, HAProxy and nginx.
   - Prefer official documentation and upstream repositories. Say explicitly when a conclusion is based on community reports.

5. Prepare changes safely:
   - Back up the current configs and write down the rollback command.
   - Keep the active SSH port allowed before changing the firewall policy.
   - Check the config before restarting.
   - Apply one layer at a time: endpoint, intermediate node, routing, DNS, then client automation.
   - Never print UUIDs, private keys, subscription links, panel credentials or certificates.

6. Check each layer:
   - Service state and listening sockets.
   - Config syntax.
   - TLS/SNI and transport handshake.
   - Public IP directly and through the proxy.
   - DNS resolution path and leaks.
   - TCP and UDP/QUIC where they are needed.
   - Persistence after reboot, failover and rollback.

7. Deliver an operational runbook:
   - Assumptions and the chosen topology.
   - Placeholders and secrets the user fills in.
   - Ordered commands and configs.
   - A check after every destructive or state-changing step.
   - Rollback steps and known limitations.

## Selection rules

- Manage Xray through Remnawave: Panel stores Config Profiles, users and subscriptions, Nodes run Xray. How this is configured is the job of skill `remnawave`.
- For a minimal fixed L4 relay, use iptables DNAT/MASQUERADE.
- For health checks, several backends or managed balancing, use HAProxy.
- Use Xray on an intermediate VPS (an intermediate Node) only when domain-based routing justifies terminating TLS, the extra CPU and the latency.
- Use Reality only on direct paths to the endpoint. Do not put Reality behind an ordinary CDN that needs the real SNI.
- For paths through a CDN, use a real domain, valid TLS, termination on nginx or similar, and a transport the CDN supports (WS, gRPC; XHTTP with caveats). Cloudflare limitations: skill `cloudflare`.
- Route through WARP selectively, not globally, unless the user explicitly asks for a global WARP exit.

## Configuration discipline

- In final Xray configs, use valid JSON: no comments, all placeholders filled in.
- Inbound/outbound tags are unique, and routing rules go from specific to fallback.
- Enable sniffing only when domain-based routing requires it, and explain the privacy implications.
- Bind internal Xray/CDN backends to loopback or a Unix socket.
- Restrict panel and statistics listeners; do not expose them publicly by default.
- Firewall rules must match the real SSH, panel, inbound, HTTP challenge and transport ports.
- For router-based setups, prevent routing loops: exclude the proxy endpoint, local networks, router addresses and management paths from transparent proxying.

## DPI and TSPU

The reference gives a diagnostic model: determine the layer from the symptoms (DNS, IP, SNI/TLS, fingerprint, shaping, UDP/QUIC) and choose a topology. The skill's sources contain no detailed description of how exactly DPI recognizes specific protocols. Mark such claims as unconfirmed and tie them to the network, date and client version.

## Reference

[references/architecture-guide.md](references/architecture-guide.md): diagnostics by symptom, topology options, direct entry, cascades (iptables, HAProxy, intermediate Node), selective WARP, router, CDN, security, acceptance and typical failures.

## Related skills

- Networking fundamentals (DNS, MTU, NAT, TLS, routing): skill `network`.
- Configuring Panel, Nodes, Config Profiles, Hosts and subscriptions: skill `remnawave`.
- Publishing through Cloudflare, ports, WebSocket and gRPC through a CDN: skill `cloudflare`.
- Before the final decision on the topology, run skill `detection-audit`: choosing direct, cascade or CDN changes the server-side detection signals.

## Boundaries

- Support legitimate goals: personal privacy, access, resilience, research and administration.
- Do not help compromise someone else's infrastructure, steal credentials, hide malware, run unauthorized scans or bypass controls on systems the user does not own or administer.
- Warn that local law, provider terms, hosting policy and employer policy may apply.
