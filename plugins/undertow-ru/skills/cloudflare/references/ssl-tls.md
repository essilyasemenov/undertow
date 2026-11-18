# Cloudflare SSL/TLS

Режим шифрования между клиентом, Cloudflare edge и origin.

## Базовая модель

- Edge certificate — сертификат, который Cloudflare показывает посетителю.
- Origin certificate — сертификат, который origin показывает Cloudflare.
- Режим SSL/TLS определяет, как Cloudflare соединяется с origin, а не только то, что видит браузер пользователя.

## Режимы SSL/TLS

- `Automatic SSL/TLS`: режим по умолчанию. Cloudflare сам подбирает самый безопасный режим, который выдерживает origin, и переводит на него трафик постепенно (от 1%, затем шагами по 10%), откатывая при ошибках. На менее безопасный режим сам не понижает: если сертификат origin истёк, `Full (strict)` останется, и следить за сертификатом нужно самому.
- `Off`: HTTPS не используется.
- `Flexible`: HTTPS только между клиентом и Cloudflare; от Cloudflare до origin идёт HTTP. Использовать крайне осторожно и не рекомендовать как целевую конфигурацию.
- `Full`: HTTPS между Cloudflare и origin есть, но сертификат origin не проверяется вообще: он может быть самоподписанным, просроченным или с CN/SAN, не совпадающим с hostname. Origin должен принимать HTTPS на порту 443 и отдавать какой-либо сертификат, иначе ошибка `525`.
- `Full (strict)`: как `Full`, но сертификат origin должен быть не просрочен, выпущен публичным CA или Cloudflare Origin CA и содержать CN или SAN, совпадающий с запрошенным hostname. Иначе ошибка `526`.
- `Strict (SSL-Only Origin Pull)`: только Enterprise. К origin всегда идёт TLS, независимо от схемы запроса посетителя; сертификат проверяется как в `Full (strict)`.

Режим можно переопределить для части запросов через Configuration Rules (значения API: `off`, `flexible`, `full`, `strict`, `origin_pull`).

## Предпочтительный подход

- По умолчанию рекомендовать `Full (strict)`.
- Для origin использовать Cloudflare Origin CA или корректный публичный сертификат.
- Если origin — это Nginx Proxy Manager, Caddy или Nginx перед Remnawave Panel, считать его обычным reverse proxy на стороне origin: Cloudflare завершает внешнее TLS-соединение на edge, а reverse proxy принимает соединение от Cloudflare так, как требует выбранный режим.

## Edge certificates

- `Universal SSL` — автоматические edge-сертификаты Cloudflare для активированных доменов.
- Учитывать ограничения покрытия Universal SSL, особенно для поддоменов второго и более глубоких уровней.
- Если нужны дополнительные имена, выбор CA или другие параметры edge-сертификата, это описано в документации Advanced Certificate Manager и Custom certificates.

## Origin certificates

- `Cloudflare Origin CA` предназначен только для соединения от Cloudflare до origin.
- Origin CA не надо описывать как сертификат для прямых клиентских подключений в обход Cloudflare.
- Если запись `DNS only`, клиент идёт прямо к origin, поэтому сертификат должен быть доверенным для самого клиента, а не только для Cloudflare.
- Публичный сертификат (например, Let's Encrypt) за `Proxied` hostname: HTTP-01-проверке мешают `Always Use HTTPS` (перенаправляет и путь `/.well-known/acme-challenge/*`; вместо неё нужен redirect rule с исключением этого пути) и Cloudflare Access на этом hostname (запрос проверки уходит на логин Access). Для origin за Access надёжнее DNS-01 или Cloudflare Origin CA.

## Рабочий процесс

1. Определить, идёт ли трафик через `Proxied`-имя или напрямую.
2. Определить, кто завершает TLS на origin: само приложение, Nginx, Caddy, Nginx Proxy Manager или другой reverse proxy.
3. Выбрать режим SSL/TLS.
4. Отдельно проверить, покрывает ли edge-сертификат нужное имя и действителен ли сертификат origin.
5. Если origin нужно защитить сильнее, рассмотреть Authenticated Origin Pulls как дополнительный слой.

## Что не делать

- Не рекомендовать `Flexible` как долгосрочную безопасную схему.
- Не путать Universal SSL с сертификатом на origin.
- Не считать Origin CA валидным ответом для прямого `DNS only` доступа посетителя.
- Не придумывать названия переключателей Nginx Proxy Manager, которых нет в документации.
- Не рассчитывать, что `Automatic SSL/TLS` спасёт от истёкшего сертификата origin.
