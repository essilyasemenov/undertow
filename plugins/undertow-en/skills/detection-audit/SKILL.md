---
name: detection-audit
description: "Audit of VPN/proxy setups for detection signals (VPN detection audit) based on the bundled methodology: GeoIP, ASN, hosting, IP reputation, DNS, routing, MTU, Android/iOS/desktop signals, latency (SNITCH), HTTP headers, false positives and the limitations of the methodology. Use before the final decision on a censorship-circumvention setup, Remnawave Nodes and Hosts, split tunneling, cascades, CDN publishing and router-based proxying, and also when asked \"is the VPN noticeable\", \"how does our setup look to a check\", detection risk, fingerprint. Bundled sources only, no external ones."
license: MIT
---

# detection-audit

Analysis of censorship-circumvention setups from the point of view of the VPN and proxy detection methods described in this skill's bundled sources.

Answer in English.

## Mandatory rules

- Use only the materials from `sources/`, `references/official/` and `references/analysis/`.
- Do not use external sites, articles, forums, documentation or your own unconfirmed knowledge as a source of facts.
- If the bundled files contain no confirmation, say directly that the claim is not supported by the skill's materials.
- Do not replace the content of the sources with guesses.
- Always distinguish a direct restatement of the source from an analytical conclusion.

## When to apply

Before a final decision or recommendation, if the task concerns:

- VPN, proxy, VLESS, Reality, XHTTP, Xray;
- Remnawave Nodes, Hosts, routing and subscription delivery;
- Cloudflare, CDN, VPS cascades;
- split tunneling and router-based proxying;
- circumventing blocking.

For an independent check of a finished setup, it can be delegated to the `detection-auditor` subagent: it works only from these materials.

## What to analyze

1. Server-side signals:
   - country and region GeoIP;
   - ASN;
   - the hosting or data center flag;
   - IP reputation, VPN/proxy/TOR lists;
   - anomalies between sessions.
2. Direct client-side signals:
   - system VPN signals on Android;
   - proxy settings on Android and iOS.
3. Indirect client-side signals:
   - interface names;
   - DNS;
   - routing;
   - MTU;
   - split tunneling.
4. Platform specifics: Android, iOS, macOS, Linux, Windows.
5. Additional methods: latency analysis (SNITCH), HTTP headers.
6. The router scenario: proxying moved from the device to the router.
7. For Remnawave infrastructure: what the check sees at the Node's egress address and which signals remain on the client.

## How to work

1. Classify the setup:
   - full VPN on the device;
   - proxy on the device;
   - split tunneling;
   - proxy only inside an app;
   - router-based proxying;
   - mixed setup.
2. Rate the detection signals by strength:
   - strong direct signals;
   - strong server-side signals;
   - indirect signals;
   - signals acceptable only as supporting ones.
3. Check separately:
   - GeoIP, ASN, hosting and IP reputation;
   - DNS, routes and MTU;
   - Android, iOS and desktop signals;
   - the risk of false positives;
   - the weak points of the methodology itself.
4. Summarize the result using the matrix in section `9` ([decision-matrix.md](references/official/decision-matrix.md)) and state which row the setup belongs to.
5. Produce a report using the template [final-report-template.md](references/final-report-template.md).

## Special focus

### Android and iOS

- For Android, consider the direct system VPN and proxy flags separately, as well as indirect signals.
- For iOS, keep in mind that direct detection is limited and proxy settings and indirect signals matter more.

### Router-based proxying

- If proxying is moved to the router, note separately that local artifacts on the device may be absent.
- At the same time, check whether risk remains from server-side factors, routing, DNS or application scenarios from the bundled materials.
- Do not claim that the router scenario fully rules out detection if the bundled files do not confirm this.

### Remnawave

- The server-side stage is assessed by the egress address of the Node through which traffic goes to the checking service.
- Splitting routes changes stage 1 but does not remove the client-side signals of stages 2a and 2b.
- Details: [remnawave-infrastructure.md](references/analysis/remnawave-infrastructure.md). How to change the configuration is the job of skill `remnawave`.

## Weak points of the methodology

Always point out:

- the limitations of GeoIP;
- the limitations of reputation databases;
- the difficulty of interpreting DNS, MTU and routes without additional confirmation;
- the ambiguity of indirect signals;
- situations in which a home, corporate, mobile or CDN scenario may look like a VPN/proxy;
- the methodology's gap regarding router setups, virtual machines and containers.

## False positives

Always check and explicitly list the risk of false positive conclusions if the setup includes:

- a corporate VPN;
- antivirus and security products;
- virtualization and containers;
- NAT, CGNAT and mobile networks;
- CDNs and global services;
- manually configured DNS;
- legitimate proxy scenarios.

## Which files to read

| Needed | File |
| --- | --- |
| Server-side signals and ports | [official/detection-signals.md](references/official/detection-signals.md) |
| GeoIP, ASN, hosting, the stage 1 algorithm | [official/geoip-asn-hosting.md](references/official/geoip-asn-hosting.md) |
| Stages and the decision matrix | [official/decision-matrix.md](references/official/decision-matrix.md) |
| Android and iOS | [official/mobile-device-detection.md](references/official/mobile-device-detection.md) |
| macOS, Linux, Windows | [official/desktop-detection.md](references/official/desktop-detection.md) |
| Latency, HTTP headers, alternative geolocation | [official/additional-methods.md](references/official/additional-methods.md) |
| False-positive scenarios | [official/false-positives.md](references/official/false-positives.md) |
| Limitations of the methodology | [official/methodology-limitations.md](references/official/methodology-limitations.md) |
| Analysis of weak points | [analysis/weak-points.md](references/analysis/weak-points.md) |
| Analysis of the router scenario | [analysis/router-based-proxy.md](references/analysis/router-based-proxy.md) |
| Analysis for Remnawave | [analysis/remnawave-infrastructure.md](references/analysis/remnawave-infrastructure.md) |
| Where the claims come from | [source-map.md](references/source-map.md) |
| Full text of the methodology | [sources/text/ocr_methodika_vpn_proxy.md](sources/text/ocr_methodika_vpn_proxy.md) |

`sources/text/ocr_methodika_vpn_proxy.md` is an English translation of the Russian-language document "Methodology for detecting signs of the use of censorship-circumvention tools on client devices", 15 pages. The Russian original (a scanned PDF and its OCR text) ships with the `undertow-ru` plugin. The translation follows the OCR text: it inherits the corrected typos of the original, the restructured table 1 and the missing document title. In a dispute over wording, the Russian PDF takes priority. The document is undated. It is a snapshot; the skill does not check whether it is still current.
