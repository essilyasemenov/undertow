# Cloudflare Tunnel

Connecting a service to Cloudflare without publishing the origin IP address and without an inbound port on the router or firewall.

## Base model

- `cloudflared` opens only an outbound connection from the origin to Cloudflare.
- Tunnel is responsible for the network path between the origin and Cloudflare.
- Identity, Access policies, Cloudflare One Client and service tokens belong to [zero-trust.md](zero-trust.md), not to this section.
- Do not describe Tunnel as "an ordinary A record pointing to a home IP": it is a separate connection model.

## Typical scenarios

- Publishing a self-hosted web application under a public hostname.
- Publishing a home panel or dashboard (for example, Remnawave Panel) without opening an inbound port.
- Connecting a private network (CIDR) to Cloudflare through Tunnel.
- Connecting a local service to Cloudflare without direct inbound access to the origin.

## Workflow

1. Determine what is needed: a public hostname or a route into a private network.
2. If the service must be reachable from the Internet as a web application, publish it through a public hostname on top of Tunnel.
3. If the service must be reachable only by authorized users or devices, first design the path through Tunnel, then add the layer from [zero-trust.md](zero-trust.md) if needed.
4. Pin down which local service is published and over which protocol.
5. Check Tunnel separately from DNS, the Access policy and the application on the origin.

## Practical rules

- For a home lab, Tunnel is usually safer than publishing the origin IP address.
- For private access through Cloudflare Zero Trust, design not only Tunnel but also a separate policy layer.
- If the task is "hide the home origin and do not open a port", consider Tunnel first.
- Do not mix a public hostname for browser access with private network (CIDR) routing: these are different Cloudflare Tunnel features.
- gRPC through Tunnel is supported only with private subnet routing; it is not supported through a public hostname.

## What not to do

- Do not describe Tunnel as requiring a publicly routable IP on the origin.
- Do not treat a proxied DNS record and Tunnel as one mechanism.
- Do not invent ingress settings that are not in the official documentation.
