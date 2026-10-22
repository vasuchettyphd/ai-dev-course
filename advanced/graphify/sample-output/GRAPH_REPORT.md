# Graph Report - deal-screener  (2026-10-22)

## Corpus Check
- Corpus is ~19,679 words - fits in a single context window. You may not need a graph.

## Summary
- 641 nodes · 1427 edges · 28 communities (21 shown, 7 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.87)
- Token cost: 40,340 input · 0 output

## Community Hubs (Navigation)
- Agent Loop
- Eval Harness
- Buy Box Rules
- Listing Extraction
- Screening Tool Input
- Deal Calculator
- CLI Main Tests
- Answering Notes
- CLI Tests Fakes
- Docs Bugs and Notes
- Eval Case Loading
- Client Setup Tests
- Notes CLI Errors
- Listing Encoding Tests
- Cost and Embed Client
- Embeddings and Similarity
- MCP Server
- MCP Server Tests
- Notes Index
- Chunk Similarity
- Note Chunking
- Note Loading
- Env File Loading
- Field Scoring
- Pinned Packages
- Contractor Etiquette

## God Nodes (most connected - your core abstractions)
1. `FakeClient` - 38 edges
2. `analyse()` - 26 edges
3. `run_with()` - 26 edges
4. `reply()` - 25 edges
5. `extract_listing()` - 24 edges
6. `FakeClient` - 22 edges
7. `run_listing()` - 21 edges
8. `ListingStepTest` - 21 edges
9. `check()` - 20 edges
10. `listing_b()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `ToolSchemaTest` --uses--> `Listing`  [INFERRED]
  tests/test_tools.py → dealscreener/calculator.py
- `main()` --indirect_call--> `text()`  [INFERRED]
  dealscreener/evaluate.py → tests/test_agent.py
- `no_package()` --calls--> `ExtractionError`  [EXTRACTED]
  tests/test_evaluate.py → dealscreener/extract.py
- `Property tax reassessment on sale` --conceptually_related_to--> `Monthly operating costs`  [INFERRED]
  notes/property-tax-reassessment.md → PLAN.md
- `Riverside condo association dues` --conceptually_related_to--> `Monthly operating costs`  [INFERRED]
  notes/riverside-association-dues.md → PLAN.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cash flow calculation components** - plan_monthly_cash_flow, plan_monthly_operating_costs, plan_monthly_mortgage_payment, plan_vacancy_rate, plan_repairs_reserve [EXTRACTED 0.95]
- **Listing B analysis documents** - listings_listing_b_brick_ranch, notes_insurance_quote_landlord_policy, notes_listing_b_write_up_decision, bugs_bug_1_small_percent_misread [INFERRED 0.85]

## Communities (28 total, 7 thin omitted)

### Community 0 - "Agent Loop"
Cohesion: 0.07
Nodes (11): AgentResult, AgentStopped, main(), print_cost(), run_agent(), run_tool(), EvalError, LiveAgentTest (+3 more)

### Community 1 - "Eval Harness"
Cohesion: 0.05
Nodes (24): CaseResult, cost_line(), main(), run_cases(), score_line(), show(), summarise(), today() (+16 more)

### Community 2 - "Buy Box Rules"
Cohesion: 0.07
Nodes (22): BuyBox, check(), _check_cash_flow(), _check_cash_on_cash(), money(), passes(), percent(), RuleResult (+14 more)

### Community 3 - "Listing Extraction"
Cohesion: 0.10
Nodes (10): extract_listing(), ExtractionError, usable_number(), ExtractListingTest, FakeClient, reply(), ListingStepTest, no_key() (+2 more)

### Community 4 - "Screening Tool Input"
Cohesion: 0.10
Nodes (7): check_input(), screen_listing(), ToolInputError, CheckInputTest, listing_b(), ScreenListingTest, ToolSchemaTest

### Community 5 - "Deal Calculator"
Cohesion: 0.12
Nodes (13): analyse(), Assumptions, _check_amount(), _check_inputs(), _check_percentage(), Listing, monthly_mortgage_payment(), EdgeCaseTest (+5 more)

### Community 6 - "CLI Main Tests"
Cohesion: 0.15
Nodes (9): FakeAPIError, FakeClient, MainTest, reply(), run(), RunAgentTest, text(), thinking() (+1 more)

### Community 7 - "Answering Notes"
Cohesion: 0.09
Nodes (10): answer(), Answer, answer_reply(), AnswerTest, ConnectError, FakeConsole, FakeGoogleError, MainTest (+2 more)

### Community 8 - "CLI Tests Fakes"
Cohesion: 0.11
Nodes (5): FakeConsole, listing_b_with_rate(), run_with(), RunTest, SmallPercentTest

### Community 9 - "Docs Bugs and Notes"
Cohesion: 0.09
Nodes (28): Bug 1: Interest rate 0.07 read as 0.07%, parse_answer (dealscreener/__main__.py), SmallPercentTest (tests/test_main.py), Listing B brick ranch ($150,000), Messy listing condo ($139,900), Landlord insurance quote ($1,200/yr), Loss of rent cover, Lender down payment notes (+20 more)

### Community 10 - "Eval Case Loading"
Cohesion: 0.12
Nodes (5): is_amount(), load_cases(), IsAmountTest, LoadCasesTest, LoadInjectionCasesTest

### Community 11 - "Client Setup Tests"
Cohesion: 0.13
Nodes (5): make_client(), MainTest, no_package(), MakeClientTest, LiveExtractTest

### Community 12 - "Notes CLI Errors"
Cohesion: 0.18
Nodes (8): describe_google_error(), http_status(), is_connection_error(), is_google_failure(), main(), run_ask(), run_index(), show_notes_instead()

### Community 13 - "Listing Encoding Tests"
Cohesion: 0.16
Nodes (4): encode_listing(), FakeClient, EncodeListingTest, PromptTest

### Community 14 - "Cost and Embed Client"
Cohesion: 0.16
Nodes (6): cost_usd(), make_embed_client(), NotesError, save_index(), KeysAndErrorsTest, no_google_key()

### Community 15 - "Embeddings and Similarity"
Cohesion: 0.20
Nodes (5): embed_texts(), normalise(), EmbedTextsTest, fake_vector(), FakeEmbedClient

### Community 17 - "MCP Server Tests"
Cohesion: 0.26
Nodes (3): McpServerTest, talk_to_server(), text_of()

### Community 18 - "Notes Index"
Cohesion: 0.26
Nodes (4): build_index(), check_fresh(), load_index(), IndexTest

### Community 19 - "Chunk Similarity"
Cohesion: 0.28
Nodes (4): Chunk, cosine(), top_chunks(), SimilarityTest

### Community 21 - "Note Loading"
Cohesion: 0.42
Nodes (3): load_notes(), LoadNotesTest, write()

### Community 24 - "Pinned Packages"
Cohesion: 0.50
Nodes (4): anthropic 1.13.0, google-genai 2.30.0, mcp[cli] 2.3.0, Pinned Python packages

## Ambiguous Edges - Review These
- `Messy listing condo ($139,900)` → `Riverside condo association dues`  [AMBIGUOUS]
  listings/messy-listing.txt · relation: conceptually_related_to

## Knowledge Gaps
- **13 isolated node(s):** `parse_answer (dealscreener/__main__.py)`, `SmallPercentTest (tests/test_main.py)`, `Cap rate`, `grill-me and Superpowers tutorial`, `Open questions (management cost, near-miss flag, closing costs)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 181 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** - run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `analyse()` connect `Deal Calculator` to `Buy Box Rules`, `Screening Tool Input`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `FakeClient` (e.g. with `ListingStepTest` and `AnswerTest`) actually correct?**
  _`FakeClient` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `parse_answer (dealscreener/__main__.py)`, `SmallPercentTest (tests/test_main.py)`, `Cap rate` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Agent Loop` be split into smaller, more focused modules?**
  _Cohesion score 0.06646825396825397 - nodes in this community are weakly interconnected._
- **Why does `FakeClient` connect `Listing Extraction` to `Agent Loop`, `CLI Tests Fakes`, `Answering Notes`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Should `Eval Harness` be split into smaller, more focused modules?**
  _Cohesion score 0.05129561078794289 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges - the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Messy listing condo ($139,900)` and `Riverside condo association dues`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._