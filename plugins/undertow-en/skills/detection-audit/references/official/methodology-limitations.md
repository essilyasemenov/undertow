# Limitations of the methodology

This file contains only the limitations directly stated in the methodology.

## Limitations of GeoIP

See section `5.6. Limitations of GeoIP`:

- mobile networks;
- CGNAT;
- corporate networks;
- border regions;
- CDNs and global services;
- user proxies with an ordinary home IP;
- reputation databases lagging behind;
- roaming.

## Limitations of mobile analysis

See section `6.6. Limitations of Mobile devices`:

- residential proxies;
- scenarios with an ordinary external provider IP;
- privacy and filtering systems that the OS does not mark as a VPN.

## Limitations of indirect signals

See sections `7.3.`, `7.6.`, `7.7.`, `7.9.`:

- indirect signals alone are not enough for a decision;
- routing does not give an unambiguous conclusion;
- DNS is not independent evidence;
- split tunneling, proxy-in-app and custom implementations make detection harder.

## Limitations of breadth of coverage

See sections `8.3.` and `8.7.`:

- extending the methodology to desktop and UNIX platforms requires accumulating statistics;
- the methodology does not consider the situation where the VPN is deployed on the user's router;
- the methodology does not consider the situation where the VPN or proxy is deployed inside a virtual machine or container.
