# DNS

Use this section when the problem looks like "the Internet works, but sites do not open by name", and when you need to explain the difference between a recursive resolver and an authoritative nameserver.

## Simple explanation

DNS translates domain names into IP addresses. Without DNS, people would have to remember the IP of every service.

## Technical explanation

DNS is a distributed, hierarchical application protocol standardized in RFC 1034 and RFC 1035. The client usually asks a recursive resolver, which in turn talks to the root, TLD and authoritative servers, using its cache and a sequence of queries.

## History

- DNS replaced centralized hosts files.
- RFC 1034 and RFC 1035 remain the base documents for the architecture and the protocol format.

## Components

- stub resolver on the client
- recursive resolver
- root servers
- TLD servers
- authoritative nameserver
- zone
- record types
- caching

## DNS in detail

### RFCs and normative basis

- RFC 1034 - Concepts and Facilities
- RFC 1035 - Implementation and Specification
- RFC 2181 - Clarifications to the DNS Specification
- RFC 2308 - Negative Caching
- RFC 7766 - DNS over TCP requirements

### Basic diagram

```text
application
  -> stub resolver
    -> recursive resolver
      -> root
      -> TLD
      -> authoritative server
    <- answer from cache or iterative lookups
```

### Recursive vs Authoritative

| Role | What it does | Typical example |
| --- | --- | --- |
| Stub resolver | Builds the query on behalf of the application | libc/systemd-resolved |
| Recursive resolver | Finds the answer and caches it | `1.1.1.1`, the provider's resolver |
| Authoritative server | Holds the zone data | the domain's NS |

### Linux commands

```sh
dig example.com
dig @1.1.1.1 example.com
dig +trace example.com
dig NS example.com
resolvectl status
tcpdump -ni any 'port 53'
```

### Practical diagnostic examples

#### Checking the resolver against authoritative data

```sh
dig @1.1.1.1 example.com
dig +trace example.com
```

If the public resolver answers `SERVFAIL` and the `+trace` chain breaks above the authoritative level, the problem is not on the client.

#### Checking split DNS

Query the name through the internal and the external resolver and compare the answers.

### Real network scenarios

#### Scenario 1. Access by IP works, by name does not

This is a typical DNS incident: the resolver does not answer, a forwarder is broken, the firewall blocks `53/udp`, or the upstream resolver is misconfigured.

#### Scenario 2. Only some clients get the wrong IP

Often the cause is the cache of a particular recursive resolver or split-horizon DNS (different answers for different networks).

### Common mistakes

- Confusing the recursive resolver with the authoritative nameserver.
- Checking DNS only by the browser symptom without `dig`.
- Ignoring the TCP/53 fallback for large answers.
- Forgetting about negative caching.

### Diagnostic order

1. Check reachability of the resolver by IP.
2. Check a query to a specific resolver with `@server`.
3. If needed, run `dig +trace`.
4. Check the local OS cache and the recursive resolver's cache.
5. Check the firewall, MTU and the TCP/53 fallback for large answers.

### Cross-references

- DNS transport: `tcp-vs-udp.md`
- Basic IP connectivity: `tcp-ip.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| DNS | The Domain Name System | Map a name to data | A hierarchy of servers returns records by domain name | Convenience for users | Dependence on distributed infrastructure | `example.com -> 93.184.216.34` | The browser opens a site by name, not by IP | Runs on top of IP |
| Recursive resolver | A server that resolves a name on behalf of the client | Take the complexity off the client | Looks up the answer at upstream servers and caches the result | Caching and convenience | May become a SPOF or a source of stale cache | `1.1.1.1` | A corporate resolver answers all office clients | Talks to authoritative servers |
| Authoritative DNS | The server that owns the zone data | Be the source of truth for the domain | Holds the official records of a specific zone | Control over the zone | Does not resolve the whole Internet for the client | NS for a domain | A change of an A record is published in the site's zone | The basis of a DNS zone |
| Zone | An administrative unit of DNS data | Structure names and records | Contains a set of records under zone management | Manageability | An error in the zone breaks resolution | `example.com` zone | An admin changes the domain's MX and TXT records | Stored on the authoritative server |

## Examples

### Example 1. Recursive resolution

The user opens `www.example.com`. The local client asks the provider's resolver or a public resolver. It finds the A/AAAA record from its cache or through iterative queries.

### Example 2. A problem with names only

```sh
ping 1.1.1.1        # works
ping example.com    # does not work
dig example.com     # timeout
```

Most likely the problem is not general IP connectivity but DNS.

### Example 3. An authoritative error

`dig @1.1.1.1 example.com` returns `SERVFAIL`, and `dig NS example.com` shows wrong NS records or a broken DNSSEC setup/zone. This is no longer the user's problem but the domain's.
