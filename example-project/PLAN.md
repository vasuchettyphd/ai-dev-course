# Plan: Rental deal screener

The instructor's worked example for week 4, in the course's fixed outline. The buy-box rules and the three numbers come from the deal screener in [the `/grill-me` and Superpowers tutorial](../advanced/grill-me-superpowers/README.md) (section 2, "Try it yourself: grill your buy box", and section 3, "Try it yourself: build the deal screener"). The 10% minimum return and the 5% vacancy are the answers given in that tutorial's sample round; the "cash flow above $0" rule is the instructor's own addition. The formulas are the standard definitions of each number.

## Goal

Type in one rental listing's numbers and, in under a minute, see its monthly cash flow, cap rate and cash-on-cash return, and whether it passes my buy box. If it fails, say which rule it failed and by how much, so I can screen listings quickly and only look closely at the ones that pass.

## Who it's for

Me: a first-time small investor looking at single-family homes and small multi-unit rentals, who wants to say no to bad deals fast. One user, on one laptop. No one else's data.

## Must-haves

1. **Inputs for one listing:** purchase price, monthly rent, yearly property tax, yearly insurance, monthly HOA fee (0 if none), down payment (%), interest rate (%), loan term (years), and closing costs ($).
2. **Assumptions I set once:** vacancy 5% of rent, and a repairs reserve as a % of rent (I pick the number; see open questions).
3. **The three numbers, with these formulas:**
   - Effective monthly rent = monthly rent x (1 - vacancy rate)
   - Monthly operating costs = (property tax + insurance) / 12 + HOA + repairs reserve
   - Monthly mortgage payment = the standard fixed-rate loan payment on (price - down payment), at my interest rate, over my loan term
   - **Monthly cash flow** = effective monthly rent - monthly operating costs - monthly mortgage payment
   - **Cap rate** = (effective monthly rent - monthly operating costs) x 12 / purchase price
   - **Cash-on-cash return** = monthly cash flow x 12 / (down payment + closing costs)
4. **The buy-box check:** pass only if cash-on-cash return is at least 10% and monthly cash flow is above $0. Show each rule, the listing's number, and pass or fail.
5. **Tests that prove the math:** at least one example listing whose answers are worked out by hand first, and a check that the tool gets exactly those answers (week 5 builds this with Superpowers, test first).

## Not in this version

- Appreciation (the home's value going up). The tutorial asks whether it should count; for now it doesn't.
- Income tax, depreciation and selling costs.
- Ranking or comparing several listings side by side.
- Pulling listings from websites automatically. I type the numbers in.
- A website, logins or a phone app.
- AI features. Ideas for later (weeks 9 to 12): explain a failed deal in plain English, or read the numbers out of a pasted listing description.

## Data it uses

- Numbers I type in for each listing, copied from public listings or made up for practice.
- My buy-box settings (minimum 10% cash-on-cash, cash flow above $0, 5% vacancy, the repairs reserve).
- No personal data: no names, addresses of people, account numbers or credit details. A listing's street address is optional and never needed for the math.

## First three build steps

1. **The calculator for one listing:** take the inputs and return the three numbers, with a hand-checked example listing as the first test.
2. **The buy-box check:** pass or fail against my rules, with the reason for each rule.
3. **A simple way to run it:** type a listing's numbers when asked, or read a small spreadsheet (CSV file) of listings, and print the results.

## Open questions

- How big should the repairs reserve be: 5%, 8% or 10% of rent?
- Should property management be a cost, as a % of rent, even if I manage it myself?
- (From the tutorial's round 3.) Should "close but not quite" deals (for example, 9% cash-on-cash) be flagged, and how close counts?
- (From the tutorial's round 3.) When two deals both pass, which number decides: cash flow or cash-on-cash return?
- Should closing costs be a fixed dollar amount or a % of the price?
