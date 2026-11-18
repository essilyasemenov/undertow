# REST API

API Tokens, built-in API documentation, controller structure and safe work with the official specification.

## Theory

- Official interactive API documentation: `https://docs.rw/api`.
- All routes are prefixed with `/api`; authorization is `Authorization: Bearer <token>`.
- Since version 2.2.0, `API Tokens` are in `Remnawave Settings`.
- Tokens support scopes: per-resource rights in the form `<resource>:read`, `<resource>:write` or `<resource>:*`. `GET /api/tokens/scopes` returns the list of available scopes.
- Scope resources (`libs/contract/api/controllers-info.ts`): `users` (including bulk operations), `hwid-user-devices`, `subscription`, `subscriptions`, `nodes`, `node-plugins`, `node-ssh`, `node-integrations`, `bandwidth-stats`, `connections`, `config-profiles`, `internal-squads`, `external-squads`, `hosts`, `subscription-template`, `subscription-settings`, `infra-billing`, `system`, `keygen`, `subscription-request-history`, `snippets`, `remnawave-settings`, `subscription-page-configs`, `metadata`, `auth`, `passkeys`, `api-tokens`. For example, a read-only token for users is `users:read`.
- When creating a token (`POST /api/tokens`), `name` (2–30 characters) and `expiresInDays` (≥ 1) are required. If `scopes` is not passed, `["*"]` is granted by default, which is full access.
- The public subscription controller `/api/sub/...` requires no authorization and is intended only for client requests.

## Built-in documentation

In 3.x the variables `IS_DOCS_ENABLED`, `SWAGGER_PATH` and `SCALAR_PATH` no longer exist. Panel always publishes:

- Swagger UI: `/api/backend-tools/swagger`;
- Scalar: `/api/backend-tools/scalar`.

Both paths are protected by separate backend tools authorization (a cookie signed with `APP_SECRET`). The docs do not describe how to get access from the panel interface; it is visible only in the `remnawave/backend` code.

## Controllers

Routes of `remnawave/backend` 3.4.11 (`libs/contract/api`), all under `/api`:

| Controller | Path |
| --- | --- |
| Users | `users` |
| API Tokens | `tokens` |
| Hosts | `hosts` |
| Config Profiles | `config-profiles` |
| Nodes | `nodes` |
| Node Plugins | `node-plugins` |
| Internal / External Squads | `internal-squads`, `external-squads` |
| Snippets | `snippets` |
| Subscriptions (protected) | `subscriptions` |
| Subscription (public) | `sub` |
| Subscription Templates / Settings | `subscription-templates`, `subscription-settings` |
| Subscription Page configs | `subscription-page-configs` |
| Subscription Request History | `subscription-request-history` |
| HWID | `hwid` |
| Remnawave Settings | `remnawave-settings` |
| System, Auth, Keygen, Metadata, Bandwidth stats, Infra billing | `system`, `auth`, `keygen`, `metadata`, `bandwidth-stats`, `infra-billing` |
| Connections, Node SSH, Node integrations, Passkeys | `connections`, `node-ssh`, `node-integrations`, `passkeys` |

## Example operations

Confirmed in the backend contract:

- `GET /api/tokens`, `POST /api/tokens`, `DELETE /api/tokens/{uuid}`, `GET /api/tokens/scopes`;
- `GET /api/users`, `POST /api/users`, `PATCH /api/users`, `GET /api/users/{id}`, `DELETE /api/users/{id}`;
- `GET /api/users/by-username/{username}`, `GET /api/users/by-short-uuid/{shortUuid}`;
- `POST /api/users/{id}/actions/enable`; alongside it `disable`, `reset-traffic`, `revoke`, `extend` (methods of the others are in the specification);
- bulk operations `POST /api/users/bulk/...` (`update`, `delete`, `reset-traffic`, `extend-expiration-date`, `update-squads` and others);
- `GET /api/hosts`, `POST /api/hosts`, `PATCH /api/hosts`, `GET /api/hosts/{uuid}`;
- `GET /api/config-profiles`.

User routes are addressed by the numeric `id` (`userId`), Hosts and tokens by `uuid`. The exact request body and response DTO are described in the official specification and may change between versions.

## SDK

The official SDKs are described in docs.rw (SDK section): TypeScript, Python, Go, plus XTLS-SDK for working with Xray. The API contract is the source of truth; the SDKs are wrappers around it.

## Practice

1. Create an API Token in `Remnawave Settings` with the minimum scopes needed.
2. Determine the class of operations: public subscription, protected admin operations, settings/tokens/tooling.
3. Method, body and response come from the official specification; this reference does not pin them down.
4. For automation and Subscription Page, pass the token through an environment variable (`REMNAWAVE_API_TOKEN`) instead of writing it into code.

## Mistakes

- Enabling the built-in documentation through `IS_DOCS_ENABLED` in 3.x: the variable no longer exists.
- Inventing endpoints that are not in the official specification.
- Putting the user's `uuid` into routes that need the numeric `id`.
- Creating a token without `scopes`: by default that is full access.
- Giving a token all scopes when read access is enough.
- Mixing the public `/api/sub` with protected admin operations.
- Hard-coding the request/response schema without checking it against the specification.
