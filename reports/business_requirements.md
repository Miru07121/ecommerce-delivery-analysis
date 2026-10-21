# Business requirements and acceptance criteria

**Stakeholder:** hypothetical operations manager and customer experience lead.
**Decision:** select delivery segments for investigation and define a measurable pilot.

| Requirement | Acceptance criterion | Implementation |
|---|---|---|
| Trust order totals | Exactly one mart row per source order; values reconcile | Unique SQL index, key and sum assertions |
| Define service performance | Denominator and same-day promise treatment documented | Eligibility flag, calendar-day SQL and boundary tests |
| Compare customer outcomes | Missing reviews excluded; review duplicates handled | Latest-review window; explicit counts and Wilson intervals |
| Prioritize work | Show both count and rate, minimum sample size | SQL queue and dashboard controls |
| Avoid misleading attribution | Multi-seller orders excluded from seller queue | Seller-count filter and caveat |
| Reproduce results | Source hashes and executable pipeline | Official downloader, quality report, tests |
| Explain a decision | Findings, next evidence, owner and evaluation plan | Management brief |

**Out of scope:** causal impact estimation, real-time deployment, current Canadian market benchmarks, profit forecasts and an actual Power BI report.

**Follow-up questions for a real stakeholder:** What promise is communicated at checkout? Is the estimated date a date or a deadline timestamp? Are promises revised? Which team controls handoff versus transit? Are survey triggers standardized? What are the costs of complaints, refunds and interventions?
