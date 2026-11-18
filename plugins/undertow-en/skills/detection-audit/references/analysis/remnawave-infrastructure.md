# Remnawave infrastructure from the methodology's point of view

This document contains analytical conclusions
and is not a direct restatement of the source.

## Purpose

The methodology is written from the checking side's position and describes client devices. This file translates its signals into the language of a Remnawave operator: which decisions about Nodes, Hosts and routing affect which signals a check will see. How Remnawave, Xray and the client apps work is not described here; skill `remnawave` covers that.

## What the GeoIP stage sees

Basis: `official/geoip-asn-hosting.md`, section `5.4`.

Stage 1 checks the external IP of the client session. If the user's traffic to the checking service goes through a Node, this IP will be the Node's egress address.

Analytical conclusions:

- Country, ASN, the hosting flag and reputation are assessed for the Node's address, not the user's.
- Per section `5.4`, a hosting flag or being in VPN/proxy/TOR lists gives "VPN detected" regardless of country. So a Node with a Russian IP in a data center does not by itself remove the stage 1 risk.
- If traffic to such a service goes directly, bypassing the Node, the check sees the user's ordinary provider IP. Splitting routes (what goes through the Node and what goes directly) is the operator's main lever for stage 1.

## The discrepancy between sections 5.4 and 9

Basis: `official/geoip-asn-hosting.md`, `official/decision-matrix.md`.

Section `5.4` calls the hosting flag sufficient for the decision "VPN detected", while the matrix in section `9` gives "additional check required" when only GeoIP is detected. Analytically: `5.4` describes the decision within stage 1, and `9` the final decision across all stages. In a report, give both levels and do not present the stage 1 decision as the final one.

## Client-side signals do not depend on the Node

Basis: `official/detection-signals.md`, `official/mobile-device-detection.md`, `official/desktop-detection.md`.

- Direct signals (`IS_VPN`, `TRANSPORT_VPN`, the system proxy) and indirect ones (`tun`/`utun`/`wg` interfaces, MTU, routes, DNS) are created by the client app on the device, not by the server.
- Splitting routes removes the stage 1 signal for a specific service, but does not remove the signals of stages 2a and 2b. Per the matrix in `9`, the combination "GeoIP not detected + direct + indirect" gives "additional check required", and "GeoIP not detected + direct only" gives "circumvention not detected".
- Which mode (TUN or system proxy), DNS and MTU the client gets is set by the configuration the subscription delivers. Assess it here only by the signals from the official files. How exactly to change it is the job of skill `remnawave`.

## Latency and cascades

Basis: `official/additional-methods.md`, section `10.1`.

- The `SNITCH` method compares the IP geolocation with the RTT to control points.
- Analytically: each additional link (a Node → Node cascade, a CDN path) increases the RTT. The further the actual path is from the stated geolocation of the egress IP, the higher the risk of an anomaly.
- The methodology gives no latency thresholds. Quantitative conclusions cannot be drawn.

## HTTP headers

Basis: `official/additional-methods.md`, section `10.2`.

- If the chain has an HTTP proxy layer that adds `X-Forwarded-For`, `Forwarded` or `Via` to the user's requests to external services, this is a signal per section `10.2`.
- The headers of the reverse proxy in front of Panel and Subscription Page concern only requests to the Panel itself and do not end up in users' traffic to external services.
- The bundled materials do not describe which specific protocols and inbound types add such headers.

## False-positive scenarios on the operator side

Basis: `official/false-positives.md`, `official/methodology-limitations.md`.

- The methodology itself admits that legitimate corporate VPNs terminate in data centers and may look like a circumvention tool by GeoIP (section `5.6`). This is a limitation of the methodology, not a protection: it explains why stage 1 gives false positives, but does not make a particular Node invisible.
- The methodology does not describe how an IP gets into reputation lists or how quickly the lists are updated, apart from a general remark about them lagging behind. Conclusions about a particular IP being "clean" are not supported by the materials.

## What the methodology does not cover

- Detection at the provider network level (DPI, protocol analysis, SNI) is not considered in the methodology. Conclusions about such detection are not supported within this skill.
- The server side of Remnawave itself (Panel, API, Subscription Page) is not mentioned in the methodology.
