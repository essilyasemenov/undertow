# Router-based proxying

This document contains analytical conclusions
and is not a direct restatement of the source.

## Purpose

This file is for analyzing situations where the circumvention logic is moved from the end device to the router or a network point close to it.

## Analytical framework

The methodology directly states only one basic limitation: it does not consider the case where the VPN is deployed on the user's router, and in such a scenario local artifacts may be absent on the client device.

Within this repository, the following can be inferred analytically from this:

- some client-side signals on the device become less observable;
- the significance of server-side factors does not disappear;
- the router scenario requires a separate analysis, not a mechanical transfer of conclusions from the "VPN on the device" scenario.

## Router solutions

Router firmware and proxying add-ons are mentioned in this file as an analytical reference to a type of architecture, not as a quote from the methodology.

Use them as a label for a class of scenarios:

- proxying and routing are moved to the router;
- the device may have no local VPN flags;
- detection through client APIs may weaken;
- server-side signals from GeoIP, ASN, hosting and IP reputation remain significant.

## How to analyze such setups

1. First separate client-side signals on the device from server-side signals.
2. Then check which local artifacts may actually be absent.
3. After that, assess whether server-side risk remains from GeoIP, ASN, hosting, IP reputation and session history.
4. Mark separately that a conclusion about the setup being completely "invisible" is not supported by the methodology alone.

## A cautious conclusion

The correct analytical conclusion for this file:

- router-based proxying may weaken client-side detection on the device;
- this is not enough to automatically consider the setup safe from all detection methods;
- the final assessment must be built on a combination of the official signals and an explicit statement of the methodology's gaps.
