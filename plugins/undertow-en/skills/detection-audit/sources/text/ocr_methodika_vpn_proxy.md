English translation of the Russian-language document "Methodology for detecting signs of the use of censorship-circumvention tools on client devices". The Russian original (scanned PDF and OCR text) ships with the `undertow-ru` plugin; in a dispute over wording, the Russian PDF takes priority.

# 1. Purpose of the document

This methodology proposes a unified approach to detecting VPN and Proxy on user devices that are used to bypass the blocking of resources prohibited by Roskomnadzor (RKN).

The methodology describes the main stages of detecting VPN and Proxy and the detection methods used, and also defines the order in which the methodology is implemented.

Besides the methods themselves, it considers the existing limitations and difficulties in applying them that are related to false positives.

# 2. Terms and abbreviations

| Term | Definition |
|---|---|
| **VPN** | A technology for creating an encrypted tunnel, in which part or all of a device's traffic is sent through a remote server. |
| **Proxy** | An application-level intermediary (HTTP proxy, SOCKS proxy, etc.) through which network requests pass. |
| **GeoIP** | Determining the geographic location (country, region, city) by IP address using specialized databases or external APIs. |
| **ASN** | *Autonomous System Number* — the identifier of a network in global routing (BGP). Allows determining the owner of an IP address and the type of network. |
| **Split tunneling** | A VPN mode in which only the traffic of selected applications is sent through the tunnel, while the rest of the traffic goes directly. |
| **Software** | Software |

# 3. General description of the methodology and the order of its implementation

There are three main areas whose analysis makes it possible to detect the use of a VPN on a client device:

- Analysis of client sessions on the server (GeoIP);
- Analysis of network connections and interfaces on the client device;
- Analysis of system settings and routing tables on the client device.

Using one or several methods of detecting the use of circumvention tools does not give a 100% guarantee of an accurate result because of possible false positives. The reasons for such situations are considered in section 4.

Analysis of client sessions on the server consists of comparing the connection IP address with a reputation database. The advantages of the method include:

- **Universality.** The analysis can be applied regardless of the operating system (OS) of the client device;
- **Transparency for the client.** The check is performed on the server side and does not require changing the client application.
- **Speed.** Fast implementation compared with other methods.
- **Simplicity.** The checks are relatively simple.

Taking these advantages into account, analysis of client sessions on the server should be implemented as the first stage of implementing VPN detection methods on client devices.

A more detailed description of the analysis of client sessions on the server is given in section 5.

To increase detection accuracy, checks on client devices should be implemented as the second stage. Since more than half of client devices are mobile devices running Android and iOS, and 80% of the applications that can be used to detect circumvention tools are installed on these devices, the analysis of network connections and interfaces and the analysis of system settings and routing tables on the client device should be implemented in this segment. Implementing checks on devices running other OSes should be assigned to subsequent, later stages.

The implementation of checks on client devices should be split into two sub-stages. In the first sub-stage, direct checks indicating the use of VPN and Proxy should be implemented. The second sub-stage aims to increase the accuracy of detecting VPN and Proxy and reduce the level of false positives by implementing indirect signs of VPN and Proxy use. Detailed descriptions of the analysis methods on client devices are given in sections 6 and 7.

The final stage aims to achieve the maximum breadth of coverage of client devices. A detailed description of the analysis methods and the existing problems for this stage is given in section 8.

**Table 1. Stages of implementing the methodology for detecting censorship-circumvention tools on client devices**

| Stage | Name | Description |
|---|---|---|
| 1 | GeoIP | Detecting VPN use on the server side by comparing the IP with reputation databases |
| 2a | Mobile devices | Analysis of direct signs of VPN use on Android and iOS |
| 2b | Accuracy | Analysis of indirect signs of VPN use on Android and iOS |
| 3 | Breadth of coverage | Analysis on the remaining client devices |

# 4. False positives and ways to minimize them

When the algorithm is applied, there may be situations where signs interpreted as VPN/Proxy use arise in legitimate device usage scenarios.

The main sources of false positives:

- **Corporate VPN.** Devices connected to a corporate network through a work VPN to access internal resources.
- **Antivirus software and security tools.** Some antivirus programs and firewalls create virtual interfaces or change routing to filter traffic.
- **Docker, WSL2, Hyper-V, VirtualBox, QEMU/KVM, Android Emulator** and other virtualization and containerization environments that create virtual adapters, routes and private subnets.
- **NAT** may cause GeoIP databases to determine the exit point in a region different from the device's location because of how connectivity is organized.

The list of measures to minimize false positives is given below:

- **Building whitelists.** Creating and maintaining a database of known corporate VPNs and legitimate proxy servers.
- **Analysis of connection dynamics.** Taking historical data into account. If a device uses a corporate VPN during working hours and turns it off outside them, such a scenario can be identified and excluded.
- **Verification by ports and protocols.** Additional analysis of the ports and tunneling protocols used. Corporate VPNs often use standard ports (for example, 443 for SSL VPN), while circumvention services may use special or dynamic ports.
- **Repeated check after a delay.** If an unambiguous decision cannot be made, it is recommended to repeat the analysis after some time to rule out temporary anomalies of the network connection.
- **Combining with other data sources.** Using additional factors: the device's GPS data, cell tower information, the history of previous successful authentications.

# 5. Stage 1: GeoIP

## 5.1. Goals of the stage

The goal of the check is to determine the geolocation of the device, obtained by comparing the IP address of the traffic entry point with data from specialized reference databases (GeoIP).

## 5.2. Scope

Analysis of client sessions is performed on the server side.

The analysis covers all devices, as well as client connections via the web.

## 5.3. GeoIP data sources

The reference database must be the system "Registry of Internet Address and Numbering Resources" (RANR).

Until it is put into operation, the use of alternative databases is allowed. The most widely used of them are MaxMind and IP2Location.

To increase the accuracy of the analysis, connecting additional commercial or internal data sources is allowed.

## 5.4. Scenarios for detecting censorship-circumvention tools

Signs used in GeoIP analysis:

- determining the country and region by IP address;
- detecting anomalies: frequent changes of country, abrupt changes of location between sessions;
- determining the ASN and the organization that owns the IP. Comparing with ranges allocated to data centers and hosting providers;
- checking reputation lists: VPN/Proxy addresses, TOR exit nodes, public Proxies;
- checking ranges against "whitelists" of corporate networks and CDNs to reduce false positives.

Algorithm for applying the methodology:

1. Determine the external IP of the client session on the server side.
2. Determine the GeoIP by this IP address.
3. Determine the ASN, the network type and whether there is a hosting flag.
4. Check the address against VPN, proxy and TOR reputation lists.
5. Compare the obtained data with the history of past sessions, typical countries, regions and trusted ranges.
6. If client-side analysis results are available, compare them with the GeoIP.
7. Decide on the use of censorship-circumvention tools based on the results of steps 1–6:
   - According to the server-side and client-side checks, the device is in the Russian Federation, there are no signs of hosting and no reputation risk. Decision: **VPN not detected**.
   - Server-side check: the device is abroad; client-side check: the device is in the Russian Federation. Decision: **VPN detected**.
   - According to the server-side and client-side checks, the device is abroad. Decision: **Additional check required**.
   - According to the server-side check, the IP has a hosting flag or is in the subnet lists of VPN, proxy and TOR. Decision: **VPN detected** regardless of whether the country matches.

## 5.5. Alternative sources of device location

An alternative source of device location data is determining the location by mobile network base station identifiers, PLMN, or by Wi-Fi access points, BSSID, followed by a GeoIP lookup. The coordinates are calculated by approximation from the known coordinates of infrastructure objects.

If the user has consented to the application using geolocation data, this data can also be used in the analysis. Using coordinates cannot replace the GeoIP check, but only complements it.

Using coordinates increases the accuracy of the analysis to reduce the level of false positives.

Coordinates do not prove the absence of VPN use.

## 5.6. Limitations of GeoIP

- GeoIP has limited accuracy for mobile networks, CGNAT, corporate networks and border regions.
- Legitimate corporate VPNs often terminate in a data center and may be identified by GeoIP as censorship-circumvention tools.
- CDNs and global services may distort the device's location without a VPN being used.
- User Proxies may have the IP of an ordinary home provider and not be detected by ASN and hosting.
- New VPN servers appear faster than reputation databases are updated.
- Geolocation changes when roaming. When the user is roaming, the Internet exit point may be in the country of stay, which creates a GeoIP mismatch.

# 6. Stage 2a: Mobile devices

## 6.1. Goals of the stage

The goal of the check is to analyze direct signs of the use of censorship-circumvention tools on mobile devices running Android and iOS.

## 6.2. Scope

Analysis of client sessions is performed on the client device.

The analysis is performed on Android and iOS mobile devices.

## 6.3. General principles of analyzing direct signals on client devices

Direct signs of the use of circumvention tools are the system VPN and Proxy indicators in Android and iOS. The signs are collected by an application on the client device through system APIs within standard user privileges.

The check must be performed when the application starts or at authentication, or when a key action is performed in the application (confirming a purchase/transfer, specifying the end point of a route, etc.). What counts as a key action in an application is decided by its developer.

Continuous monitoring or sending empty analysis results is prohibited, because it would negatively affect the traffic usage and battery consumption of the client device.

The analysis on client devices does not depend on the server-side analysis and is an independent check; nevertheless, the main task of the analysis is to confirm and/or refine the data obtained during the GeoIP analysis.

## 6.4. Android

For Android, the system APIs `ConnectivityManager` and `NetworkCapabilities` are used. The proposed approaches do not require `root` access and must work with standard application privileges.

Direct signs of VPN use are:

- the `IS_VPN` flag in `Score(Policies)`;
- a `VPN` transport in `Transports`;
- the presence of `VpnTransportInfo`;
- the `TRANSPORT_VPN` property on `activeNetwork` when checking `hasTransport`.

Examples of diagnostic values:

```text
Score(Policies: ):
EVER_EVALUATED&IS_UNMETERED&IS_VPN&EVER_VALIDATED&IS_VALIDATED
Transports: WIFI|VPN
VpnTransportInfo{type=1, sessionId=PCAPdroid VPN, bypassable=false
longLiveTcpConnectionsExpensive=false}
```

To detect a Proxy, `System.getProperty` and other available system settings should be analyzed. If the system settings contain the IP and port of a Proxy, all traffic is probably sent through it.

List of characteristic Proxy ports for different technologies:

- `SOCKS`: `1080, 9000, 5555, 16000-16100`;
- `http`: `80, 443, 3128, 3127, 8000, 8080, 8081, 8888`;
- transparent Proxies: `80, 443, 4080, 7000/7044, 8082, 12345`;
- `Tor`: `9050, 9051, 9150`.

## 6.5. iOS

On iOS, access to system data is significantly restricted. Therefore using direct signs on iOS is very difficult. Analysis of direct signs is possible only if the application itself creates configurations that may be regarded as censorship-circumvention tools.

To detect the use of a system Proxy, the system API `CFNetworkCopySystemProxySettings()` should be used to get the settings of the current connection.

The presence of an IP and port indicates a Proxy and that all device traffic is sent through it.

## 6.6. Limitations of Mobile devices

- Residential proxies and scenarios where the external IP looks like an ordinary provider address.
- Privacy and filtering systems, if the OS does not mark them as VPN.

# 7. Stage 2b: Accuracy

## 7.1. Goals of the stage

The goal of the check is to analyze indirect signs of the use of censorship-circumvention tools on mobile devices running Android and iOS.

## 7.2. Scope

Analysis of client sessions is performed on the client device.

The analysis is performed on Android and iOS mobile devices.

## 7.3. General principles of analyzing indirect signals on client devices

Indirect signs of the use of circumvention tools are interface names, MTU values, routing table anomalies and changed DNS. Indirect signs can also arise when the device is used without circumvention tools. Therefore using indirect signs alone when making a decision is not acceptable. Indirect signs are used only to increase the accuracy of the VPN and Proxy detection result.

Indirect signs are collected as part of a single process of collecting data about the client device.

## 7.4. Android

As an indirect sign, the `NOT_VPN` flag in `Capabilities` can be checked. For ordinary networks this flag is present; when a VPN is active, it is absent.

```text
without VPN. Transports: WIFI Capabilities:
NOT_METERED&INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VPN&VALIDATED&NOT_ROAMING
&FOREGROUND&NOT_CONGESTED&NOT_SUSPENDED&NOT_VCN_MANAGED

with VPN. Transports: WIFI|VPN Capabilities:
NOT_METERED&INTERNET&NOT_RESTRICTED&TRUSTED&VALIDATED&NOT_ROAMING&FOREGRO
UND&NOT_CONGESTED&NOT_SUSPENDED&NOT_VCN_MANAGED
```

The interface names `tun0`, `tun1`, `tap0`, `wg0`, `ppp0`, `ipsec` may indicate an active VPN connection and are indirect signs, because interfaces with similar names can be created by antivirus programs, content filters, corporate security tools, system components and other services.

Another tool for collecting indirect signs on Android 12+ is service data such as `dumpsys vpn_management` and `dumpsys activity service`, which provide a list of active VPNs with the package name.

```text
VPNs:
  0: io.github.romanvht.byedpi
     Active package name: io.github.romanvht.byedpi
     Active vpn type: 1

ServiceRecord{... io.github.romanvht.byedpi/.services.ByeDpiVpnService}
intent={act=android.net.VpnService ...}
```

## 7.5. iOS

On iOS there are the following ways to detect indirect signs of the use of censorship-circumvention tools:

- Analysis of system proxy settings through `CFNetworkCopySystemProxySettings()`.
- Analysis of the `__SCOPED__` key and the list of active interfaces.
- Using `NWPathMonitor` to track changes in the network state.
- Using `NEVPNManager` in those scenarios where the application is entitled to use it and has the corresponding rights.

The `CFNetworkCopySystemProxySettings()` function returns a dictionary with the current settings. The `__SCOPED__` key contains the names of active interfaces. The presence of interfaces named `utun`, `tap`, `tun`, `ppp`, `ipsec` may indicate a running VPN.

The `P2P` parameter set in the interface parameters may serve as an indirect sign. `NWPathMonitor` makes it possible to track network state changes in real time. In the `pathUpdateHandler`, the `path.availableInterfaces` list can be analyzed for interfaces of type `.other` with a name containing `utun`.

We single out `NEVPNManager` as a separate extended tool for detecting indirect signs. It provides detailed information only about those VPNs that were configured through the application itself or are available to the application under the `NetworkExtension` model. Using it requires special rights, `entitlements`. Thus `NEVPNManager` is of limited use and cannot solve the problem of detecting VPN in general.

The built-in `iCloud Private Relay` service deserves separate mention. This service must not be automatically classified as a prohibited VPN, although using it does make it possible to bypass blocking. Working with this service requires separate handling logic to reduce the risk of false positives.

## 7.6. Routing

Below are anomalies in device routing tables that indirectly indicate VPN use:

- A default route pointing to an interface other than the main physical or wireless one.
- Dedicated routes that send traffic to non-standard gateways.
- No direct route to the ISP's gateway while a connection is active.
- Non-standard MTU values.
- Routes indicating split tunneling, where part of the traffic goes through the tunnel and part goes directly.

These signs can complement checks on the server side or the analysis of direct signs on the client device. Detecting only these signs is not grounds for the decision "VPN detected".

Reasons that limit the use of routing analysis for detecting VPN:

- The private ranges `10.0.0.0/8`, `172.16.0.0/12` and `192.168.0.0/16` are found everywhere in office, home and container environments.
- Route metrics change automatically depending on the environment and are not a unique sign of VPN.
- Multiple interfaces and virtual routes are created by WSL2, Hyper-V, VirtualBox, antivirus programs, parental control tools and other legitimate components.

Below are anomalies in device routing tables that indirectly indicate Proxy use:

- The default route is configured to send traffic to a virtual network interface;
- Dedicated routes in the routing table.
- A large number of established connections to a local port;
- Clients using random ports;
- No direct external connections.

Routing table analysis is not applicable to iOS, because applications' access to information about other applications and system settings is restricted.

## 7.7. DNS

Analysis of DNS settings is also an indirect sign. An explicit change of the DNS server to a public address, or DNS inside the VPN network, can be a refining sign, but is not sufficient on its own.

Reasons that limit the use of DNS settings analysis for detecting VPN:

- DNS can be changed without a VPN, for example by filtering or ad-blocking applications.
- The user may set DNS manually, for example a public or corporate one.
- Some VPNs do not change DNS and leave the DNS of the parent network.
- Local DNS addresses and DNS directed to a virtual interface are useful only in combination with other signs.

Below are anomalies in DNS settings that indirectly indicate Proxy use:

- DNS servers are assigned local addresses;
- All DNS queries are directed to a virtual network interface.

## 7.8. Additional technical methods for detecting Proxy

- Checking for specialized utilities, for example `proxychains` or `tsocks`.
- Detecting system processes of proxy servers by process names and characteristic ports.
- Analyzing firewall rules, `iptables` or `pf`, for redirections to a local proxy.
- Monitoring active connections to non-standard or remote ports.
- Checking local certificates and signs of a Man in the Middle proxy.

## 7.9. Limitations of Accuracy

- In split tunneling mode some applications may work directly, so a check by one active network is not sufficient.
- Proxy-in-app, custom tunnels and user implementations of circumvention that are not reflected in system APIs.

# 8. Stage 3: Breadth of coverage

## 8.1. Goals of the stage

The goal of the check is to analyze direct and indirect signs of the use of censorship-circumvention tools on any client devices.

## 8.2. Scope

Analysis of client sessions is performed on the client device.

The analysis is performed on devices with operating systems other than Android and iOS.

## 8.3. Challenges of Breadth of coverage

Extending the methodology for detecting censorship-circumvention tools to client devices running Windows, the UNIX family and MacOS involves certain difficulties. On the one hand, the use of applications on these devices is insignificant compared with mobile devices. On the other hand, these devices use technologies that are not typical of mobile devices but may lead to false positives.

Taking the above arguments into account, the decision to extend the breadth of device coverage should be applied after implementation and after accumulating certain statistical data on the effectiveness of detecting circumvention tools.

Detection methods for these devices should also be developed after the first stages are completed.

## 8.4. MacOS

Specifics of detecting the use of circumvention tools on MacOS:

- Analyzing interfaces through `getifaddrs()` makes it possible to enumerate network interfaces, including virtual ones.
- Analyzing the routing table makes it possible to detect non-standard traffic routing.
- `Transparent Proxy API` is a separate type of network path that may be useful for detection.
- `Network Extensions` system extensions require explicit user permission.
- Forced routing `enforceRoutes` can be considered an additional technical sign.

## 8.5. UNIX and Linux

Specifics of detecting the use of circumvention tools on UNIX/Linux:

- Characteristic interface names: `tun`, `tap`, `wg`, `utun`, `ppp`.
- Only active interfaces with the `UP` status and an assigned IP address are used.
- For VPN tunnel interfaces, the MTU is often lower than the standard values, for example `1350` or `1400`.
- The presence of several default routes, routes through virtual interfaces, atypical subnets and changed DNS can be used as additional analysis.
- Analyzing `/etc/resolv.conf` and other DNS configurations is useful only as a supporting factor.
- Comparing local and public IP addresses, as well as the address belonging to a data center, are also additional signs.

## 8.6. Windows

Specifics of detecting the use of circumvention tools on Windows:

- `RasEnumConnection` can be used to detect active remote connections.
- `GetAdaptersAddresses` or `GetAdaptersInfo` may be used to analyze network adapters.
- Signs may include the virtual adapter type, `IfType = IF_TYPE_PROP_VIRTUAL`, characteristic names VPN, TAP, Wintun, WireGuard, OpenVPN and the `UP` state.
- As an extended method, the registry can be analyzed to detect VPN and proxy settings.
- Checking the default gateway, DNS, a mismatch between the public and local IP, and interface metrics are additional accuracy factors.

For all desktop and UNIX platforms the general rule holds: interfaces, routes, MTU, private subnets and DNS by themselves are not sufficient grounds for a hard decision without server-side risk or other strong confirmation.

## 8.7. Limitations of Breadth of coverage

- The methodology does not consider situations where the VPN is deployed on the user's router. In this case there are no local artifacts on the client device, and detecting censorship-circumvention tools is difficult.
- The methodology does not consider situations where the VPN or Proxy is deployed inside a virtual machine or container running on the client device.

# 9. Criteria for deciding that circumvention tools are detected

To detect the use of circumvention tools on client devices, a comprehensive approach to decision-making is used, because no single check gives 100% accuracy.

**Table 2. Decision matrix**

| GeoIP | Direct signs | Indirect signs | Decision |
|---|---|---|---|
| NOT detected | NOT detected | NOT detected | Circumvention not detected |
| NOT detected | Detected | NOT detected | Circumvention not detected |
| NOT detected | NOT detected | Detected | Circumvention not detected |
| Detected | NOT detected | NOT detected | Additional check required |
| NOT detected | Detected | Detected | Additional check required |
| Detected | Detected | NOT detected | Circumvention detected |
| Detected | NOT detected | Detected | Circumvention detected |
| Detected | Detected | Detected | Circumvention detected |

- **Circumvention detected:** all checks did not detect VPN and Proxy use, or signs of use were detected only in one of the first two checks.
- **Additional check required:** signs of VPN use were detected in two checks, but there are contradictions between them. A repeated check with an extended set of criteria, or a manual check, is required.
- **Circumvention detected:** signs were detected in the first and second checks, and at the same time the third check established that the source IP address belongs to VPN/Proxy infrastructure or its geolocation reliably does not match the expected one.

# 10. Additional methods for detecting circumvention tools

## 10.1. Latency analysis method

An alternative method of checking that does not require external services is the latency analysis method `SNITCH` (*Server-side Non-intrusive Identification of Tunnelled Characteristics*). The method is based on measuring the response time (`RTT` — *Round-Trip Time*) between the server and the client. When traffic passes through a VPN, it takes a detour via the VPN server, which inevitably adds latency. The `SNITCH` approach combines IP address geolocation data with precise measurements of network latency to "control points" (`landmarks`). Abnormally high latency for the IP address geolocation indicates VPN use.

## 10.2. HTTP header analysis

The presence of the `X-Forwarded-For`, `Forwarded` or `Via` headers may indicate passage through an intermediate proxy node. This sign must be used with caution, because the service itself or a CDN may also legitimately set some of these headers.
