# Cloudflare Security

Protecting a web application, API or origin on the Cloudflare side.

## Current terminology

- In the current Cloudflare documentation the former `Firewall Rules` are deprecated and have been migrated to `WAF custom rules`.
- For new designs, use `WAF`, `Custom rules`, `Managed rules`, `Rate limiting rules` and `DDoS Protection`.

## Basic components

- `WAF`: inspects incoming HTTP and API traffic and applies rulesets.
- `Custom rules`: your own filtering logic with actions such as `Block` and `Managed Challenge`.
- `Managed rules`: ready-made Cloudflare rulesets.
- `Rate limiting rules`: limiting request rate by an expression and client characteristics.
- `Bot protection`: protection against unwanted bots and related rules.
- `DDoS Protection`: automatic L3/L4/L7 protection on the Cloudflare side.

## Workflow

1. Determine the threat type: vulnerability exploitation, password brute force, scraping, unwanted bots, volumetric attack, API abuse.
2. Separate ready-made protection (managed) from your own logic (custom).
3. Express new HTTP policies in terms of custom rules and the rules language.
4. For abuse that is visible by request rate, use rate limiting rules.
5. For scenarios sensitive to origin load, check whether harmful traffic reaches the origin or is dropped at the edge.

## Practical rules

- If the user asks for "firewall rules", explain through the current `WAF custom rules` model and mention the former term if needed.
- For bots, check the built-in bot protection first, and only then add complexity with custom rules.
- For password brute force and API abuse, rate limiting is a separate layer, not a replacement for WAF.
- Do not describe DDoS protection as a manual "turn protection on" switch: at Cloudflare much of it works automatically.
- Challenges are designed for a browser. The Cloudflare Challenges documentation specifically warns that an interstitial challenge affects API endpoints called by non-browser clients (`curl`, mobile backends, server-to-server), and WebView in apps may work only partially. For paths called by client apps (for example, subscription delivery), design challenge rules with this limitation in mind.

## What not to do

- Do not base new recommendations on the deprecated Firewall Rules as the main API and UI model.
- Do not promise that one custom rule replaces all managed protections.
- Do not invent rate limiting thresholds without explicitly marking them as an example rather than a rule from the documentation.
