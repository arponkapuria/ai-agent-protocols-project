## AI Agent Protols Project - Procurement Agent

**Project Scenario**

**Company:** *JAMC (Just Another Manufacturing Company)* — a mid-size manufacturer that assembles industrial equipment and needs a steady supply of components (steel bolts, bearings, gaskets, etc.).

**Problem:** Procurement is currently manual — a purchasing coordinator checks stock in a spreadsheet/ERP, emails 2–3 suppliers for quotes, waits days for replies, manually places the order, and gets manager sign-off for anything over budget. It's slow and error-prone, and nothing is tracked in one place.

**Solution:** `procurement_manager`, an AI agent that automates the full restock cycle end-to-end, while keeping a human in the loop for anything above policy limits.

**End-to-end flow**

> *User: "Check our steel bolt inventory, get quotes from both suppliers, and if we're low, order 500 units from whichever is better — auto-approve if it's under policy."*

**Stage 1 — Gather information**

- [x] **MCP →** queries the internal inventory MCP server (`check_inventory("steel_bolts")`) against a SQLite ERP table. Stock is low (ex. 40 units, reorder threshold 100).
- [ ] **A2A →** queries two independent remote agents: `vendor_pricing_agent` (today's price/lead time from each supplier) and `vendor_quality_agent` (defect rate/on-time delivery history). Supplier B comes out ahead on price and quality.

**Stage 2 — Take action**

- [ ] **UCP →** sends a typed checkout request to Supplier B's mock UCP endpoint (`/.well-known/ucp`) for 500 units, gets back an order confirmation.
- [ ] **AP2 →** the order total (\$1,200) is checked against an `IntentMandate` policy (auto-approve under \$2,000 from approved vendors). It's under the limit, so the agent signs a `PaymentMandate` itself and a `PaymentReceipt` closes the audit trail. (We'll also build the escalation path: an order over $2,000 stays unsigned and shows up as "pending manager approval" on the dashboard.)

**Stage 3 — Report results**

- [ ] **A2UI →** composes a live dashboard: current stock levels, the two suppliers compared side by side, and the order status card.
- [ ] **AG-UI →** streams the whole thing to the frontend as it happens — tool calls, quote comparisons, and the final approval/order confirmation appear incrementally, not as one big blob at the end.
