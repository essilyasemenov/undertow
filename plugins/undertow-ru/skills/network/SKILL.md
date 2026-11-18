---
name: network
description: "Фундаментальная база по компьютерным сетям (networking fundamentals) на русском: OSI, TCP/IP, TCP и UDP, MTU/MSS, NAT/CGNAT, routing, gateway, DNS и DNS security (DoH/DoT/DNSSEC), IPv4/IPv6, ports, TLS/mTLS, HTTPS, HTTP/2/HTTP/3/QUIC, CDN, anycast, BGP, reverse proxy, load balancing, firewall, Linux networking. Использовать для объяснения сетевых концепций, диагностики связности, разбора маршрутов, проблем DNS, NAT, MTU, TLS, публикации сервисов за reverse proxy/CDN и выбора транспорта, в том числе для Remnawave Panel и Node. Также Docker и firewall: опубликованные порты контейнеров, ufw и iptables, почему порт контейнера доступен снаружи, хотя закрыт в ufw."
license: MIT
---
# network

Общий вход в сетевую тематику: базовая теория, прикладная диагностика и проектирование связности. Это базовый слой для остальных skills `undertow`: `remnawave`, `cloudflare`, `architecture` и `detection-audit` опираются на него.

## Как работать с этим skill

1. Определить класс проблемы: теория, диагностика, проектирование, публикация сервиса, деградация производительности.
2. Если проблема не локализована, начать с [references/osi-model.md](references/osi-model.md).
3. Если нужна реальная стековая модель Интернета, перейти к [references/tcp-ip.md](references/tcp-ip.md).
4. Для адресации и связности использовать разделы IPv4, IPv6, routing и gateway.
5. Для проблем приложений проверять DNS, TCP/UDP, порты, NAT/CGNAT и MTU.
6. Для безопасной публикации сервисов, VPN-панелей и edge-инфраструктуры использовать TLS, HTTPS, CDN, reverse proxy, firewall и linux-networking.
7. Читать только нужный файл темы из `references/`, а не все подряд.

## Темы (`references/`)

| Тема | Файл | Когда открывать |
| --- | --- | --- |
| OSI | [osi-model.md](references/osi-model.md) | разложение проблемы по слоям |
| TCP/IP | [tcp-ip.md](references/tcp-ip.md) | практический стек Интернета |
| TCP vs UDP | [tcp-vs-udp.md](references/tcp-vs-udp.md) | выбор транспорта |
| MTU | [mtu.md](references/mtu.md) | MTU, MSS, PMTUD, фрагментация |
| NAT | [nat.md](references/nat.md) | трансляция адресов и портов |
| CGNAT | [cgnat.md](references/cgnat.md) | операторский NAT |
| Routing | [routing.md](references/routing.md) | выбор пути и маршруты |
| Gateway | [gateway.md](references/gateway.md) | шлюз по умолчанию |
| DNS | [dns.md](references/dns.md) | разрешение имён |
| DNS security | [dns-security.md](references/dns-security.md) | DNSSEC, DoH, DoT, privacy |
| IPv4 | [ipv4.md](references/ipv4.md) | адресация IPv4 |
| IPv6 | [ipv6.md](references/ipv6.md) | адресация IPv6, ICMPv6 |
| Ports | [ports.md](references/ports.md) | транспортные порты и сокеты |
| TLS | [tls.md](references/tls.md) | TLS, сертификаты, handshake |
| mTLS | [mtls.md](references/mtls.md) | двусторонняя аутентификация |
| HTTPS | [https.md](references/https.md) | HTTPS, redirects, secure publication |
| HTTP/2, HTTP/3 | [http2-http3.md](references/http2-http3.md) | multiplexing, QUIC, head-of-line blocking |
| CDN | [cdn.md](references/cdn.md) | edge caching, origin shielding |
| Anycast | [anycast.md](references/anycast.md) | выбор ближайшего edge |
| BGP | [bgp.md](references/bgp.md) | AS, path selection, междоменная маршрутизация |
| Reverse proxy | [reverse-proxy.md](references/reverse-proxy.md) | upstream routing, публикация сервисов |
| Load balancing | [load-balancing.md](references/load-balancing.md) | распределение трафика, failover |
| Firewall | [firewall.md](references/firewall.md) | фильтрация и exposure policy |
| Linux networking | [linux-networking.md](references/linux-networking.md) | interfaces, routes, sockets, link state |
| Источники | [sources.md](references/sources.md) | канонические RFC и официальная документация |

## Рабочий диагностический порядок

```text
link
  -> L2 adjacency
    -> IP address/prefix
      -> route/default gateway
        -> DNS
          -> TCP/UDP and port
            -> NAT/CGNAT
              -> MTU/MSS/PMTUD
                -> application behavior
```

## Правила качества

- Предпочитать объяснение от простого к техническому, не теряя смысла.
- При нормативных формулировках опираться на RFC.
- При практических примерах явно указывать протокол, адресное семейство, порт и направление трафика.
- Не считать рабочий `ping` доказательством исправности DNS, TCP, TLS или приложения.
- Для глубокой темы переходить в профильный файл, а не расширять ответ до энциклопедического пересказа.

## Связь с другими skills

- Продуктовые шаги Remnawave (install, nodes, subscriptions): skill `remnawave`.
- DNS, proxy/CDN, TLS-режимы и Tunnel на стороне Cloudflare: skill `cloudflare`.
- Выбор топологии (direct, cascade, CDN) в условиях блокировок: skill `architecture`.
- Если вывод влияет на видимость VPN-инфраструктуры (GeoIP/ASN, DNS, маршруты, MTU), перед финальным решением пройти skill `detection-audit`.
