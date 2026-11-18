# VPN and proxy detection signals

This file contains only the signals and mechanisms directly supported by the text of the methodology.

## Server-side signals

Section `5.4. Scenarios for detecting censorship-circumvention tools` lists:

- determining the country and region by IP address;
- detecting anomalies: frequent changes of country and abrupt changes of location between sessions;
- determining the ASN and the organization that owns the IP;
- comparing with ranges allocated to data centers and hosting providers;
- checking reputation lists of VPN, proxy, TOR and public proxies;
- checking ranges against whitelists of corporate networks and CDNs.

## Direct signals on Android

Section `6.4. Android` lists:

- the `IS_VPN` flag in `Score(Policies)`;
- a `VPN` transport in `Transports`;
- the presence of `VpnTransportInfo`;
- the `TRANSPORT_VPN` property on `activeNetwork` when checking `hasTransport`;
- analyzing `System.getProperty` and other system settings to detect a proxy;
- a proxy IP and port in the system settings.

Section `6.4. Android` also lists characteristic ports:

- `SOCKS`: `1080`, `9000`, `5555`, `16000-16100`;
- `http`: `80`, `443`, `3128`, `3127`, `8000`, `8080`, `8081`, `8888`;
- transparent proxies: `80`, `443`, `4080`, `7000/7044`, `8082`, `12345`;
- `Tor`: `9050`, `9051`, `9150`.

## Direct signals on iOS

Section `6.5. iOS` lists:

- using `CFNetworkCopySystemProxySettings()` to get the system proxy settings;
- the presence of an IP and port as a sign that traffic goes through a proxy.

## Indirect signals on Android

Section `7.4. Android` lists:

- the absence of the `NOT_VPN` flag in `Capabilities` when a VPN is active;
- interface names `tun0`, `tun1`, `tap0`, `wg0`, `ppp0`, `ipsec`;
- service data from `dumpsys vpn_management`;
- service data from `dumpsys activity service`.

## Indirect signals on iOS

Section `7.5. iOS` lists:

- analyzing the system proxy settings through `CFNetworkCopySystemProxySettings()`;
- analyzing the `__SCOPED__` key and the list of active interfaces;
- using `NWPathMonitor`;
- using `NEVPNManager` in permitted scenarios;
- interfaces named `utun`, `tap`, `tun`, `ppp`, `ipsec`;
- the `P2P` parameter in the interface parameters;
- interfaces of type `.other`, including names with `utun`;
- singling out `iCloud Private Relay` separately.

## Routing and MTU

Section `7.6. Routing` lists:

- a default route through an interface other than the main physical or wireless one;
- dedicated routes to non-standard gateways;
- no direct route to the ISP's gateway while a connection is active;
- non-standard MTU values;
- routes indicating split tunneling;
- for a proxy: a default route through a virtual interface, dedicated routes, a large number of connections to a local port, random client ports, no direct external connections.

## DNS

Section `7.7. DNS` lists:

- an explicit change of the DNS server to a public address;
- DNS inside the VPN network;
- local DNS addresses;
- DNS queries directed to a virtual interface.

## Additional technical methods

Section `7.8. Additional technical methods for detecting Proxy` lists:

- `proxychains`;
- `tsocks`;
- system processes of proxy servers;
- `iptables` or `pf` rules redirecting to a local proxy;
- active connections to non-standard or remote ports;
- local certificates and signs of a Man in the Middle Proxy.

Section `10.2. HTTP header analysis` lists:

- `X-Forwarded-For`;
- `Forwarded`;
- `Via`.
