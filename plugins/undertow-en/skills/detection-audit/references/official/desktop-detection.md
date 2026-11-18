# Signals on desktop and UNIX platforms

This file contains only the signals of the "Breadth of coverage" stage directly described in the methodology.

## macOS

Section `8.4. MacOS` lists:

- enumerating interfaces, including virtual ones, through `getifaddrs()`;
- analyzing the routing table for non-standard routing;
- `Transparent Proxy API` as a separate type of network path;
- `Network Extensions` system extensions that require explicit user permission;
- forced routing `enforceRoutes` as an additional technical signal.

## UNIX and Linux

Section `8.5. UNIX and Linux` lists:

- interface names `tun`, `tap`, `wg`, `utun`, `ppp`;
- only active interfaces in the `UP` state with an assigned IP are taken into account;
- the MTU of tunnel interfaces is often lower than the standard one, for example `1350` or `1400`;
- several default routes, routes through virtual interfaces, atypical subnets and changed DNS as additional analysis;
- `/etc/resolv.conf` and other DNS configurations only as a supporting factor;
- comparing the local and public IP and the address belonging to a data center as additional signals.

## Windows

Section `8.6. Windows` lists:

- `RasEnumConnection` for active remote connections;
- `GetAdaptersAddresses` or `GetAdaptersInfo` for analyzing adapters;
- the virtual adapter type `IfType = IF_TYPE_PROP_VIRTUAL`, the names VPN, TAP, Wintun, WireGuard, OpenVPN and the `UP` state;
- analyzing the registry for VPN and proxy settings as an extended method;
- the default gateway, DNS, a mismatch between the public and local IP, and interface metrics as additional accuracy factors.

## The general rule of section 8

Interfaces, routes, MTU, private subnets and DNS by themselves are not sufficient grounds for a hard decision without server-side risk or other strong confirmation.
