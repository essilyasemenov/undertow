---
name: cloudflare
description: "Cloudflare для публикации и защиты сервисов: edge network, Anycast, CDN, reverse proxy, Proxied (orange cloud) и DNS only (grey cloud), DNS-записи и DNSSEC, SSL/TLS-режимы (Flexible, Full, Full strict, Automatic), edge certificates и Origin CA, supported proxy ports, WebSocket, gRPC, CF-Connecting-IP, WAF, rate limiting, DDoS, Cloudflare Tunnel (cloudflared), Zero Trust, Access, Cloudflare One Client (WARP), service tokens. Использовать, когда домен, Remnawave Panel, страница подписок или транспорт Node публикуется через Cloudflare: можно ли пустить VLESS, Reality, XHTTP, WebSocket или gRPC транспорт Xray через оранжевое облако или CDN Cloudflare, какой порт выбрать, при ошибках 52x, выборе proxy status и SSL mode, скрытии origin IP. В том числе общие вопросы без привязки к проекту: чем отличаются режимы SSL/TLS (Flexible, Full, Full strict), какой выбрать, что значат ошибки 525 и 526."
license: MIT
---
# cloudflare

Как именно Cloudflare стоит между клиентом и origin. Без этой модели легко ошибиться в DNS, SSL/TLS, Tunnel или Zero Trust. Отвечать на русском языке.

## Что считать базовой моделью

- Cloudflare для веб-трафика работает как reverse proxy на своей edge-сети, а не как «универсальный TCP/UDP-прокси по умолчанию».
- Anycast нужен для того, чтобы запрос попадал в ближайшую или доступную edge-точку Cloudflare.
- CDN, кэширование, WAF и часть security-функций доступны только там, где трафик действительно проходит через edge Cloudflare.
- `Proxied` и `DNS only` — это не косметическая разница, а выбор архитектуры потока трафика.

## Ключевые термины

- `Orange Cloud` / `Proxied`: Cloudflare принимает веб-трафик на своей edge-сети, может кэшировать, фильтровать и скрывать origin IP.
- `Grey Cloud` / `DNS only`: Cloudflare только отвечает DNS-записью, а клиент идёт напрямую в origin.
- `Edge Network`: глобальная сеть точек присутствия Cloudflare, где применяются сертификаты edge, CDN и security-функции.
- `Origin`: ваш сервер или промежуточный reverse proxy, например Nginx Proxy Manager, Caddy или Nginx перед Remnawave Panel.

## Разделы (`references/`)

| Задача | Файл |
| --- | --- |
| Record types, proxy status, DNSSEC | [dns.md](references/dns.md) |
| SSL/TLS modes, edge certificates, Origin CA | [ssl-tls.md](references/ssl-tls.md) |
| Standard Proxy/CDN: кэш, порты, WebSocket, gRPC, заголовки | [proxy-cdn.md](references/proxy-cdn.md) |
| `cloudflared`, public hostnames, private network через Tunnel | [tunnel.md](references/tunnel.md) |
| Access, identity, policies, Cloudflare One Client, service tokens | [zero-trust.md](references/zero-trust.md) |
| WAF, custom rules, rate limiting, DDoS | [security.md](references/security.md) |
| Cloudflare рядом с Remnawave Panel, Node, подписками и homelab | [remnawave-integration.md](references/remnawave-integration.md) |
| Официальные ссылки по всем разделам | [sources.md](references/sources.md) |

## Рабочий процесс

1. Сначала определить тип сервиса: публичный веб-сервис, запись для верификации, почта, частный ресурс, Tunnel или нестандартный транспорт.
2. Затем определить, должен ли трафик идти через Cloudflare edge или напрямую на origin.
3. Только после этого выбирать тип DNS-записи, proxy status и режим SSL/TLS.
4. Если задача касается VPN, панели, API, self-hosted приложения или домашней сети, не считать автоматически, что стандартный прокси Cloudflare подходит для любого протокола.

## Практические правила

- Если цель — CDN, WAF, скрытие origin IP и edge certificates, нужен `Proxied` веб-трафик.
- Если цель — почта, верификация домена, часть сценариев с SRV/MX/TXT или неподдерживаемый транспорт, чаще нужен `DNS only`.
- Если нужен доступ к частному ресурсу без входящего порта, сначала рассматривать Tunnel, а затем отдельно решать, нужен ли поверх него доступ через Zero Trust.
- Если документация Cloudflare называет ограничения продукта, не заменять их предположениями «обычно должно работать».

## Что не делать

- Не описывать Cloudflare как замену любого VPN или любого L4-прокси без проверки конкретного продукта.
- Не обещать преимущества CDN или WAF для записей `DNS only`.
- Не путать origin certificate и edge certificate.
- Не придумывать поведение оранжевого облака для протоколов, которые в документации не подтверждены.

## Связь с другими skills

- Сетевая теория (DNS, TLS, CDN, anycast, reverse proxy): skill `network`.
- Настройки Remnawave (Hosts, Config Profiles, транспорты Xray): skill `remnawave`. Здесь только Cloudflare-side.
- Выбор топологии (direct, cascade, CDN) в условиях блокировок: skill `architecture`.
- Если публикация через Cloudflare влияет на видимость VPN-инфраструктуры, перед финальным решением пройти skill `detection-audit`.
