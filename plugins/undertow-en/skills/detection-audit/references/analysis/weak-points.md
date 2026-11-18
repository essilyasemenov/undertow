# Weak points of the methodology

This document contains analytical conclusions
and is not a direct restatement of the source.

## Purpose

This file collects an interpretation of the methodology's limitations for when you need not just to list the official caveats, but to understand where exactly they weaken the reliability of a conclusion.

## Main analytical conclusions

- GeoIP is convenient as an early filter but does not look like self-sufficient evidence.
- A hosting flag, the ASN and a bad IP reputation increase suspicion but do not remove the need to take context into account.
- Indirect signals are useful in combination, but individually they create a high risk of misinterpretation.
- Router setups form a confirmed gap in the methodology and require separate analysis.
- Desktop, UNIX, container and hybrid environments make the picture less clear-cut than the classic mobile scenario.

## Practical limitations of interpretation

- Matching geography does not prove the absence of a proxy or VPN.
- The absence of mobile flags does not prove the absence of circumvention.
- The presence of indirect signals does not prove the presence of circumvention.
- The same set of observations can correspond both to circumvention and to legitimate infrastructure.

## How to use this file

Use this document only after reading the files from `references/official/`.

It is needed to:

- separate officially confirmed signals from analytical interpretation;
- explicitly mark the places where a conclusion is an assessment;
- avoid mixing a direct restatement of the methodology with practical reasoning about its limits.
