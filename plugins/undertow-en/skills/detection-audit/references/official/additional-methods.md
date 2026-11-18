# Additional detection methods

This file contains only the additional methods directly described in the methodology.

## Alternative sources of location

Section `5.5. Alternative sources of device location` lists:

- location by mobile network base station identifiers (`PLMN`) or by Wi-Fi access points (`BSSID`), followed by a GeoIP lookup;
- coordinates from an app, if the user has consented to geolocation;
- coordinates do not replace the GeoIP check but complement it and reduce the number of false positives;
- coordinates do not prove the absence of a VPN.

## Latency analysis (SNITCH)

Section `10.1. Latency analysis method` states:

- the `SNITCH` method (Server-side Non-intrusive Identification of Tunnelled Characteristics) does not require external services;
- the `RTT` between the server and the client is measured;
- through a VPN, traffic takes a detour via the VPN server, which adds latency;
- the IP geolocation is compared with the latencies to control points (`landmarks`);
- abnormally high latency for the stated IP geolocation indicates a VPN.

## HTTP header analysis

Section `10.2. HTTP header analysis` states:

- the `X-Forwarded-For`, `Forwarded` or `Via` headers may indicate an intermediate proxy node;
- the signal should be used with caution: a service or CDN may legitimately set some of these headers.
