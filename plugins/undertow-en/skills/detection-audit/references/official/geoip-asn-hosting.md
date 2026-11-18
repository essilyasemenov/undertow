# GeoIP, ASN, hosting and IP reputation

This file contains only the server-side signals and limitations directly supported by the methodology.

## Goal of the stage

Section `5.1. Goals of the stage` states that the goal of the check is to determine the device's geolocation by comparing the IP address of the traffic entry point with GeoIP data.

## Scope

Section `5.2. Scope` states:

- the analysis is performed on the server side;
- the analysis covers all devices, including web connections.

## Data sources

Section `5.3. GeoIP data sources` lists:

- RANR (the Registry of Internet Address and Numbering Resources) as the reference database;
- until it is put into operation, MaxMind and IP2Location are acceptable;
- connecting additional commercial or internal sources is allowed.

## Signals of the GeoIP stage

Section `5.4. Scenarios for detecting censorship-circumvention tools` lists:

- determining the country and region by IP address;
- detecting anomalies between sessions;
- determining the ASN and the organization that owns the IP;
- comparing with data center and hosting provider ranges;
- checking VPN, proxy, TOR and public proxy lists;
- checking ranges against whitelists of corporate networks and CDNs.

## Application algorithm

Section `5.4.` gives the following order:

1. Determine the external IP of the client session.
2. Determine the GeoIP by the IP address.
3. Determine the ASN, the network type and whether there is a hosting flag.
4. Check the address against VPN, proxy and TOR reputation lists.
5. Compare the data with the history of past sessions, typical countries, regions and trusted ranges.
6. If client-side data is available, compare it with the GeoIP.

## Decisions based on the results of the stage

Section `5.4.` directly gives the options:

- the server-side and client-side checks point to Russia, there is no hosting flag and no reputation risk: VPN not detected;
- the server-side check points abroad, the client-side check to Russia: VPN detected;
- the server-side and client-side checks point abroad: additional check required;
- the IP has a hosting flag or is in VPN, proxy and TOR lists: VPN detected regardless of whether the country matches.

## Limitations of GeoIP

Section `5.6. Limitations of GeoIP` lists:

- limited accuracy for mobile networks;
- limited accuracy for CGNAT;
- limitations for corporate networks;
- limitations for border regions;
- distortions because of CDNs and global services;
- user proxies with an ordinary home IP;
- new VPN servers appearing faster than reputation databases are updated;
- geolocation changes when roaming.
