# DNS Security

## 1. What it is

`DNS security` is the practice of protecting DNS infrastructure and DNS traffic. Cloudflare describes it as a set of complementary measures: redundancy, DNSSEC and operational control. This section focuses on `DNSSEC`, `DoH` and `DoT`.

## 2. Why it is needed

- to protect DNS from spoofed answers, cache poisoning and other interference;
- to increase trust in DNS answers through `DNSSEC`;
- to protect query privacy through `DoH` and `DoT`;
- to ensure stable resolution of critical names.

## 3. How it relates to VPN infrastructure

- VPN clients and panels depend on correct DNS;
- secure DNS is especially important for subscription, panel and API domains and for upstream resolvers;
- without understanding DNSSEC, DoH and DoT it is easy to merge privacy, integrity and authenticity into one function.

## 4. How it relates to Cloudflare

- the Cloudflare Learning Center explains `DNSSEC`, `DoH` and `DoT` in detail;
- Cloudflare DNS and its anycast infrastructure often serve as an example of a public secure resolver;
- it is important to distinguish `DNSSEC` as protection of answer integrity from `DoH`/`DoT` as protection of channel privacy.

## 5. How it relates to Remnawave

- `Remnawave` depends on correct resolution of the panel, API and subscription page domains;
- secure DNS is especially important where DNS interference can break circumvention, configuration delivery or access to the panel domain.

## 6. Common mistakes

- treating `DNSSEC` as the equivalent of `DoH` or `DoT`;
- thinking encrypted DNS verifies the authenticity of answers by itself;
- forgetting that `DoT` and `DoH` still require the resolver's IP address to be reachable;
- breaking secure DNS with firewall rules or MTU problems;
- diagnosing "broken Internet" when the problem is only the path to the secure resolver.

## 7. Diagnostics

1. Determine what this is about: privacy, integrity or resolver availability.
2. Separate `DNSSEC`, `DoH` and `DoT` by purpose.
3. Check plain DNS and secure DNS separately.
4. Check the firewall, routing and MTU.
5. Check whether the problem is in the resolver's policy.

## 8. Practical examples

- Explaining the difference between `DNSSEC` and `DoH`.
- Analyzing a case where secure DNS is unstable because of problems along the path.
- Checking why the panel domain resolves through plain DNS but not through the configured secure resolver.

## 9. Checklist

- Find out what is needed: confidentiality, integrity, authenticity or all of them.
- Do not confuse DNSSEC with DoH/DoT.
- If needed, go to `dns.md`, `anycast.md` and `firewall.md`.

## Sources

- Cloudflare DNS security: <https://www.cloudflare.com/learning/dns/dns-security/>
- Cloudflare DoT vs DoH: <https://www.cloudflare.com/learning/dns/dns-over-tls/>
- RFC 4033 DNSSEC Introduction: <https://www.rfc-editor.org/info/rfc4033/>
- RFC 4034 DNSSEC Resource Records: <https://www.rfc-editor.org/info/rfc4034/>
- RFC 4035 DNSSEC Protocol Modifications: <https://www.rfc-editor.org/info/rfc4035/>
- RFC 7858 DNS over TLS: <https://www.rfc-editor.org/info/rfc7858/>
- RFC 8484 DNS over HTTPS: <https://www.rfc-editor.org/info/rfc8484/>
