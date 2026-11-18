# Cloudflare Zero Trust

Access to an application or private resource not "through an open URL for everyone", but through a model where identity and policies make the decision.

## Base model

- `Cloudflare Access` uses Access policies to define who can access an application.
- `Identity Provider` (IdP) is the source of user identity.
- `Cloudflare One Client` (formerly WARP) connects a device to the Cloudflare network and passes device data to the policies.
- `Service Tokens` are for service-to-service access and automation.
- The network path to a private resource or local service is usually set up through Tunnel ([tunnel.md](tunnel.md)); this section does not replace Tunnel and does not describe connector-level publishing.

## What to design

- Who gets access: a user, a group, a service, a device.
- What is protected: an Access application, an automation endpoint or another private resource.
- What is required to sign in: login through an IdP, mTLS, a service token or a device check through Cloudflare One Client (device posture).

## Workflow

1. Determine the resource and the access method: browser application, private name, private IP/CIDR, automation.
2. Choose the Access application type and the policy model.
3. Connect an IdP if access is granted to users.
4. If access depends on the device, decide whether Cloudflare One Client is needed.
5. For automation, decide whether a service token fits.
6. If the application model requires it, validate the Access token on the origin side too.

## Practical rules

- For an internal panel, home panel or admin interface, consider Access first rather than a public URL without authentication.
- For private network access, consider the network path, the identity layer and the client path through Cloudflare One Client separately.
- For partners, contractors and multiple identity domains, keep in mind that Cloudflare supports several IdPs at once.
- For services without interactive login, consider `Service Auth` and `Service Tokens`.

## What not to do

- Do not treat Zero Trust as simply "another VPN".
- Do not confuse a public hostname through Tunnel with private access through Cloudflare One Client: for the user these are different scenarios.
- Do not present a service token as equivalent to a user session.
- Do not skip token validation on the origin where the official documentation requires it.
