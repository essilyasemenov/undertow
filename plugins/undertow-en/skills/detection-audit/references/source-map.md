# Source map for `references/`

This file describes how traceability works now that `references/` is split into two layers:

- `references/official/` — a direct restatement and arrangement of what is supported by `ocr_methodika_vpn_proxy.md` (the English translation of the methodology; the Russian original `_VPN_proxy_.pdf` ships with `undertow-ru`);
- `references/analysis/` — analytical conclusions, interpretations and applied reasoning on top of the official layer.

## Reading principle

- if you need a fact from the methodology, use `references/official/` first;
- if you need a conclusion about weak points, gaps or the router scenario, then use `references/analysis/`;
- if you need to check where a particular claim comes from, look at this file.

## `references/official/detection-signals.md`

Source: only the methodology text (`ocr_methodika_vpn_proxy.md`).

Main source sections:

- server-side signals: `5.4. Scenarios for detecting censorship-circumvention tools`;
- Android direct signals: `6.4. Android`;
- iOS direct signals: `6.5. iOS`;
- Android indirect signals: `7.4. Android`;
- iOS indirect signals: `7.5. iOS`;
- routing and MTU: `7.6. Routing`;
- DNS: `7.7. DNS`;
- additional technical methods: `7.8. Additional technical methods for detecting Proxy`;
- HTTP headers: `10.2. HTTP header analysis`.

Status: direct official layer.

## `references/official/false-positives.md`

Source: only the methodology text (`ocr_methodika_vpn_proxy.md`).

Main source sections:

- false-positive scenarios and error-reduction measures: `4. False positives and ways to minimize them`;
- limitations of GeoIP: `5.6. Limitations of GeoIP`;
- limitations of DNS: `7.7. DNS`;
- the separate case of `iCloud Private Relay`: `7.5. iOS`.

Status: direct official layer.

## `references/official/geoip-asn-hosting.md`

Source: only the methodology text (`ocr_methodika_vpn_proxy.md`).

Main source sections:

- `5.1. Goals of the stage`;
- `5.2. Scope`;
- `5.3. GeoIP data sources`;
- `5.4. Scenarios for detecting censorship-circumvention tools`;
- `5.6. Limitations of GeoIP`.

Status: direct official layer.

## `references/official/mobile-device-detection.md`

Source: only the methodology text (`ocr_methodika_vpn_proxy.md`).

Main source sections:

- `6.3. General principles of analyzing direct signals on client devices`;
- `6.4. Android`;
- `6.5. iOS`;
- `6.6. Limitations of Mobile devices`;
- `7.3. General principles of analyzing indirect signals on client devices`;
- `7.4. Android`;
- `7.5. iOS`;
- `7.9. Limitations of Accuracy`.

Status: direct official layer.

## `references/official/methodology-limitations.md`

Source: only the methodology text (`ocr_methodika_vpn_proxy.md`).

Main source sections:

- `5.6. Limitations of GeoIP`;
- `6.6. Limitations of Mobile devices`;
- `7.3. General principles of analyzing indirect signals on client devices`;
- `7.6. Routing`;
- `7.7. DNS`;
- `7.9. Limitations of Accuracy`;
- `8.3. Challenges of Breadth of coverage`;
- `8.7. Limitations of Breadth of coverage`.

Status: direct official layer.

## `references/official/decision-matrix.md`

Source: only the methodology text (`ocr_methodika_vpn_proxy.md`).

Main source sections:

- `3. General description of the methodology and the order of its implementation`, table 1;
- `9. Criteria for deciding that circumvention tools are detected`, table 2.

Status: direct official layer. The explanations under table 2 contradict the table in the PDF itself (p. 14); this is noted in the file.

## `references/official/desktop-detection.md`

Source: only the methodology text (`ocr_methodika_vpn_proxy.md`).

Main source sections:

- `8.4. MacOS`;
- `8.5. UNIX and Linux`;
- `8.6. Windows`.

Status: direct official layer.

## `references/official/additional-methods.md`

Source: only the methodology text (`ocr_methodika_vpn_proxy.md`).

Main source sections:

- `5.5. Alternative sources of device location`;
- `10.1. Latency analysis method`;
- `10.2. HTTP header analysis`.

Status: direct official layer.

## `references/analysis/weak-points.md`

Source: an analytical document.

Basis for the analysis:

- `references/official/geoip-asn-hosting.md`
- `references/official/mobile-device-detection.md`
- `references/official/false-positives.md`
- `references/official/methodology-limitations.md`

This file contains:

- an interpretation of the limitations;
- practical conclusions about the reliability of signals;
- evaluative statements about the weakness of individual methods;
- summary conclusions about the ambiguity of the result.

Status: analytical layer, not a direct restatement of the source.

## `references/analysis/router-based-proxy.md`

Source: an analytical document.

Basis for the analysis:

- `references/official/methodology-limitations.md`
- `references/official/geoip-asn-hosting.md`
- `references/official/mobile-device-detection.md`

This file contains:

- a discussion of router-based proxying as a separate architectural class;
- conclusions about the difference between a VPN on the device and moving the logic to the router;
- cautious practical reasoning about what weakens and what remains significant.

Status: analytical layer, not a direct restatement of the source.

## What changed compared with the previous structure

Everything directly supported by the PDF/OCR text was moved to `official/`:

- signals;
- mobile mechanisms;
- GeoIP/ASN/hosting;
- official limitations;
- false-positive scenarios.

Everything related to interpretation was moved to `analysis/`:

- weak points of the methodology;
- router-based proxying;
- practical limitations and cautious conclusions;
- Remnawave infrastructure from the methodology's point of view.

## `references/analysis/remnawave-infrastructure.md`

Source: an analytical document.

Basis for the analysis:

- `references/official/geoip-asn-hosting.md`
- `references/official/decision-matrix.md`
- `references/official/detection-signals.md`
- `references/official/mobile-device-detection.md`
- `references/official/desktop-detection.md`
- `references/official/additional-methods.md`
- `references/official/false-positives.md`

This file contains conclusions about how decisions on Remnawave Nodes, Hosts and routing affect the methodology's signals.

Status: analytical layer, not a direct restatement of the source.
