# Android and iOS: direct and indirect signals

This file contains only the mobile signals and limitations directly supported by the methodology.

## The general logic of the mobile stage

Sections `6` and `7` state:

- stage `2a` covers direct signals;
- stage `2b` covers indirect signals;
- the analysis is performed on Android and iOS mobile devices.

Section `6.3. General principles of analyzing direct signals on client devices` states:

- direct signals are system VPN and proxy indicators;
- they are collected by an app through system APIs within standard user privileges;
- the check is performed when the app starts, at authentication or at a key action;
- continuous monitoring and sending empty results are prohibited.

Section `7.3. General principles of analyzing indirect signals` states:

- indirect signals are interface names, MTU values, routing anomalies and changed DNS;
- using indirect signals alone when making a decision is not acceptable.

## Android

Section `6.4. Android` lists the direct signals:

- `IS_VPN`;
- `VPN` in `Transports`;
- `VpnTransportInfo`;
- `TRANSPORT_VPN` on `activeNetwork`;
- proxy settings in `System.getProperty` and other system settings;
- the presence of a proxy IP and port.

Section `7.4. Android` lists the indirect signals:

- the absence of `NOT_VPN` in `Capabilities`;
- interfaces `tun0`, `tun1`, `tap0`, `wg0`, `ppp0`, `ipsec`;
- `dumpsys vpn_management`;
- `dumpsys activity service`.

## iOS

Section `6.5. iOS` lists:

- the limitations of direct analysis;
- `CFNetworkCopySystemProxySettings()` for checking the system proxy;
- the presence of an IP and port as a sign of proxy use.

Section `7.5. iOS` lists:

- `CFNetworkCopySystemProxySettings()`;
- the `__SCOPED__` key;
- active interfaces;
- `NWPathMonitor`;
- `NEVPNManager`;
- interfaces `utun`, `tap`, `tun`, `ppp`, `ipsec`;
- the `P2P` parameter;
- the `.other` interface type;
- separate logic for `iCloud Private Relay`.

## Limitations of the mobile stage

Section `6.6. Limitations of Mobile devices` lists:

- residential proxies;
- scenarios where the external IP looks like an ordinary provider address;
- privacy and filtering systems, if the OS does not mark them as a VPN.

Section `7.9. Limitations of Accuracy` lists:

- split tunneling;
- proxy-in-app;
- custom tunnels and user implementations that are not reflected in system APIs.
