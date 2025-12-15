# Panda Financial - Growth Proposal (Israeli Market)

## Overview
To drive growth and usage for "Panda Financial" in the Israeli market, we propose a hybrid approach combining high-value utility tools (Calculators) with content aggregation (News).

## Proposed Features

### 1. Israeli Salary Calculator ("Bruto to Neto")
*   **Why:** High search volume keyword in Israel ("מחשבון שכר"). Essential for employees and job seekers.
*   **Implementation:**
    *   **Frontend:** JavaScript-based for instant results.
    *   **Backend (Optional):** Could be used to serve the latest tax brackets (Mas Hachnasa / Bituach Leumi) so they can be updated centrally without redeploying the static site.

### 2. Mortgage ("Mashkanta") Simulator
*   **Why:** Israel has a high rate of home ownership and complex mortgage tracks (Prime, Madad, Fixed/Variable).
*   **Implementation:**
    *   **Frontend:** Interactive graphs and amortization tables.
    *   **Backend:** Can store "scenarios" for users who sign up (Lead Generation).

### 3. Financial News Aggregator
*   **Why:** Users want a single place to see headlines from Globes, Calcalist, TheMarker, and Bizportal.
*   **Implementation:**
    *   **Backend:** Python crawler (leveraging existing `web_crawler` codebase) that runs periodically.
    *   **Frontend:** A feed displaying the latest headlines with links.

### 4. Currency & Stock Ticker (TA-35, ILS/USD)
*   **Why:** Real-time context for financial decisions.
*   **Implementation:** Backend service fetching from public APIs or scraping.

## Architecture Decisions

### Client-Side vs. Backend for Calculators
You asked: *Why backend if it works on client side?*

*   **Client-Side (Recommended for MVP):**
    *   **Pros:** Instant feedback, offline capability, lower server costs, better UX.
    *   **Cons:** Logic is exposed.
*   **Backend Role:**
    *   We should use the backend for **Growth Mechanics**:
        *   **Lead Capture:** "Email me this report."
        *   **User Accounts:** "Save my mortgage scenarios."
        *   **Data Aggregation:** The crawler service (News).

## Execution Plan
1.  Build the **News Crawler** (Python).
2.  Build the **Salary Calculator** (Client-side JS).
3.  Create a **Landing Page** integrating both.
