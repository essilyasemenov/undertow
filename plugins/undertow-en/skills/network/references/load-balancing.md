# Load Balancing

## 1. What it is

`Load balancing` is the distribution of traffic across several backend instances to increase availability, scalability and resilience. The NGINX documentation describes load balancing as distributing traffic across application servers for throughput, lower latency and fault tolerance.

## 2. Why it is needed

- to avoid overloading a single backend;
- to increase fault tolerance;
- to scale applications and panels;
- to increase the availability of public web services and APIs.

## 3. How it relates to VPN infrastructure

- web interfaces and management APIs of a VPN may need load balancing;
- subscription pages, dashboards and services behind a reverse proxy benefit from failover;
- load balancing is especially useful where availability and smooth scaling matter.

## 4. How it relates to Cloudflare

- delivery through the Cloudflare edge and distributed infrastructure are closely tied to resilience;
- Cloudflare materials directly link CDN reliability to traffic distribution and failover;
- it is important to distinguish anycast edge traffic distribution from application-level load balancing.

## 5. How it relates to Remnawave

- Panel is scaled with the `API_INSTANCES` variable (default `1`); `remnawave/backend` also has `docker-compose-advanced-prod.yml`, where the REST API is split into separate scalable services (details: skill `remnawave`);
- `Nginx Proxy Manager` and `NGINX` are the typical place where load balancing between upstreams is configured in practice.

## 6. Common mistakes

- confusing load balancing with anycast;
- expecting session stickiness to one backend without explicit configuration;
- load balancing a service whose backend is not designed for several instances;
- forgetting that health checks and failover logic change the observed behavior.

## 7. Diagnostics

1. Check whether one backend or several answer.
2. Find out whether there is session stickiness.
3. Check the expectations for failover and health checks.
4. Separate distribution at the edge from application-level load balancing.
5. Check whether the root cause is in the reverse proxy.

## 8. Practical examples

- Load balancing several web backend instances through `NGINX`.
- Analyzing why requests to the same panel give different results.
- Explaining the difference between the Cloudflare anycast edge and upstream load balancing in NGINX.
- Checking failover when one origin fails.

## 9. Checklist

- Find out what this is about: distribution through anycast/CDN or application-level load balancing.
- Determine whether there is an upstream group and failover.
- Check whether session affinity is needed.
- If needed, go to `reverse-proxy.md`, `cdn.md` and `anycast.md`.

## Sources

- NGINX HTTP load balancing: <https://nginx.org/en/docs/http/load_balancing.html>
- NGINX upstream module: <https://nginx.org/en/docs/http/ngx_http_upstream_module.html>
- NGINX documentation: <https://nginx.org/en/docs/>
- Cloudflare CDN reliability and load balancing: <https://www.cloudflare.com/learning/cdn/cdn-load-balance-reliability/>
