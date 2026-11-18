# Stages of the methodology and the decision matrix

This file contains only the stages and decision criteria directly described in the methodology.

## Implementation stages

Section `3. General description of the methodology and the order of its implementation`, table 1:

| Stage | Name | What is analyzed |
| --- | --- | --- |
| 1 | GeoIP | Server side: the IP is compared with reputation databases |
| 2a | Mobile devices | Direct VPN signals on Android and iOS |
| 2b | Accuracy | Indirect VPN signals on Android and iOS |
| 3 | Breadth of coverage | Other client devices |

The same section states:

- server-side analysis is implemented first: it is universal, does not depend on the OS, is transparent to the client, fast and simple;
- no method or combination of methods gives a 100% guarantee of accuracy because of false positives.

## Decision matrix

Section `9. Criteria for deciding that circumvention tools are detected`, table 2:

| GeoIP | Direct signals | Indirect signals | Decision |
| --- | --- | --- | --- |
| not detected | not detected | not detected | circumvention not detected |
| not detected | detected | not detected | circumvention not detected |
| not detected | not detected | detected | circumvention not detected |
| detected | not detected | not detected | additional check required |
| not detected | detected | detected | additional check required |
| detected | detected | not detected | circumvention detected |
| detected | not detected | detected | circumvention detected |
| detected | detected | detected | circumvention detected |

Section `9` also states:

- the decision is made as a whole, because no single check gives 100% accuracy;
- "additional check required" means a repeated check with an extended set of criteria or a manual check.

## A contradiction within the source

The explanations under table 2 contradict the table itself. This is how the source PDF reads (p. 14); it is not an OCR error:

- the first item is labeled "Circumvention detected", although it describes the case where no signals were found or they were found only in one of the first two checks. According to the table, this is "Circumvention not detected";
- the third item ("Circumvention detected") calls the IP belonging to VPN/proxy infrastructure the result of the "third check", although according to table 1 and section 5 this is stage 1 (GeoIP). According to the table, GeoIP plus any one client-side signal is enough for the decision "circumvention detected".

In the analysis, rely on table 2. Quote the explanations only together with a note about the contradiction.
