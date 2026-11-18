# False positives

This file contains only the false-positive scenarios and error-reduction measures directly described in the methodology.

## Sources of false positives

Section `4. False positives and ways to minimize them` lists:

- corporate VPN;
- antivirus software and security tools;
- Docker;
- WSL2;
- Hyper-V;
- VirtualBox;
- QEMU/KVM;
- Android Emulator;
- other virtualization and containerization environments;
- NAT, because of which GeoIP may determine a different region.

## Measures to reduce false positives

Section `4` lists:

- building whitelists;
- analyzing connection dynamics;
- verification by ports and protocols;
- a repeated check after a delay;
- combining with other data sources.

## Additional limitations affecting accuracy

Directly following from section `5.6. Limitations of GeoIP`:

- limited accuracy for mobile networks;
- limited accuracy for CGNAT;
- limitations for corporate networks;
- limitations for border regions;
- distortions from CDNs and global services;
- the effect of roaming;
- reputation databases lagging behind;
- scenarios where a user's proxy looks like an ordinary home IP.

Directly following from section `7.7. DNS`:

- DNS may be changed without a VPN;
- the user may set DNS manually;
- some VPNs do not change DNS;
- local DNS addresses are useful only in combination with other signals.

Directly following from section `7.5. iOS`:

- `iCloud Private Relay` must not be automatically classified as a prohibited VPN.
