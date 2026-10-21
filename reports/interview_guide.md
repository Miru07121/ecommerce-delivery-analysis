# Interview walkthrough and resume wording

## A 90-second explanation

I built an operations analytics project using Olist's public historical marketplace data. I wanted to understand where late delivery problems concentrated and how delivery status related to customer reviews. I joined seven tables into an order-level SQL mart, aggregating items and selecting one review per order to prevent duplicate counts. I checked source keys, reconciled totals and tested the date boundaries.

The analysis found that 6.77% of eligible delivered orders were late. Reviewed late orders had a much higher poor-review rate, but I found an important timing issue: restricting to review records created on or after delivery reduced the gap considerably. I presented both comparisons rather than claiming that lateness caused the full difference.

I built a dashboard to compare destination, category and seller segments by both rate and volume, and recommended investigating specific delivery lanes before proposing interventions. A real next step would need carrier scans and a prospective pilot; I did not claim financial savings from observational data.

## Questions to prepare for

- Why aggregate item records before joining reviews? Explain many-to-many fanout with two items and two reviews.
- Why is delivery at 11 pm on the promise date still on time? The project's promise is a calendar date, not a midnight cutoff.
- Why do the two review comparisons differ? Timing restrictions change the sample; selection and other confounders remain.
- Is the largest seller late-order count the worst seller? No. Compare denominators, service mix and carrier responsibility.
- Why not claim a 53-point improvement from fixing delivery? An association is not an intervention effect.
- How would you validate a notification pilot? Predefine outcomes, randomize where feasible, monitor costs and service guardrails.

## Resume bullets, after you can explain and reproduce the work

- Built a Python and SQL pipeline integrating seven public e-commerce tables into a validated 99,441-order analytical mart, with automated checks for join duplication, date boundaries and missing reviews.
- Developed an interactive delivery-performance dashboard and management brief; identified a 6.77% late-delivery rate and assessed how review timing changed customer-satisfaction comparisons.

Keep this under Projects. Do not present it as paid Olist work, real employer data, a Power BI project, or implemented cost savings. Practice modifying one query and one dashboard filter yourself before interviews.
