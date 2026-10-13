# POS Payment Processing Error

## Overview

Customers experience payment declines, card reader malfunctions, or transaction timeouts during checkout on FoodTech POS terminals despite valid payment methods. This runbook distinguishes between customer card issues and system-level payment processing failures to expedite resolution.

## Affected Systems

- **FoodTech POS v4.2.x** with Ingenico/Verifone payment terminals
- **FoodTech POS v5.1.x** with Ingenico/Verifone payment terminals
- Integrated payment terminals: Ingenico iCT220, iCT250, Verifone MX915, MX925
- Host systems: ServeWell Payment Gateway, Merchant Processor (First Data/Fiserv)

## Symptoms

- Customer card declined with no clear reason; cardholder confirms valid account and funds
- "DECLINED-INTERNAL" error codes displayed on terminal or POS screen
- Card reader unresponsive or fails to detect card insertion
- Error codes: **E201** (Payment Gateway Timeout), **E202** (Merchant Authentication Failure), **E409** (Terminal Communication Failure)
- Transaction timeout errors during payment processing (>30 seconds without completion)
- Multiple transactions failing in succession from a single terminal
- "Unable to Connect to Payment Processor" messaging
- Customer presented with generic decline message; staff unsure of root cause

## Immediate Steps (First 2 Minutes)

1. **Ask the customer**: Confirm the card is not expired, has sufficient funds, and has not been flagged for fraud. Request they try a different card or payment method (cash, mobile wallet) to determine if issue is card-specific.

2. **Check terminal hardware**: Ensure the card reader is not stuck, physically damaged, or showing error lights. Inspect cable connections at the terminal base and POS unit. Confirm the terminal is powered on (green/blue status light illuminated).

3. **Attempt a test transaction**: Request a staff member re-ring a small transaction ($0.01–$1.00 test charge if permitted by merchant account) on a known working card from a different customer or internal test account to isolate whether the issue is terminal-wide or customer-specific.

---

## L1 Diagnosis Steps

### Step 1: Gather Information

1. Note the **exact error code** displayed (E201, E202, E409, or other).
2. Record the **transaction timestamp** and **terminal ID** (located in Settings menu).
3. Ask: "Is this affecting one customer, one terminal, or multiple terminals across the location?"
4. Check if the customer is using **credit, debit, or contactless** (tap/chip/swipe).

### Step 2: Verify Customer Card vs. System Issue

1. **Customer card issue** → Customer tries alternate payment method and succeeds.
2. **System issue** → Multiple payment methods or multiple customers decline on the same terminal.

   **If customer card issue only:** Advise customer to contact their card issuer; escalate is **not needed**.

   **If system issue:** Proceed to Step 3.

### Step 3: Check Terminal and Network Connectivity

1. On the POS terminal, navigate to **Settings > System Status > Payment Terminal**.
2. Confirm **Terminal Status** shows "Connected" (not "Offline" or "Error").
3. Verify **IP Address** and **Gateway Connection** are active.
4. Note the **Last Transaction Time** and **Transaction Count** for the shift.
5. Check that the terminal displays **"Ready"** on the home screen (not "Waiting for Connection" or flashing error).

### Step 4: Verify Merchant Account and Payment Gateway

1. On the POS back-office, log in with manager credentials → **Reports > Payment Processing > Gateway Status**.
2. Confirm **Payment Gateway Status** is "Online" (green indicator).
3. Check **Merchant Account Status**—look for any flags, suspensions, or authentication warnings.
4. Note the **Last Successful Transaction** timestamp. If older than 1 hour, gateway connectivity may be degraded.
5. Review **Recent Decline Reasons**:
   - Filter by today's date.
   - Search for patterns (e.g., all declines show E201, E202, or E409).

### Step 5: Isolate the Specific Error Code

Run through the error code decision tree:

| Error Code            | Meaning                                    | Common Cause                                                   | Immediate Action                                                    |
| --------------------- | ------------------------------------------ | -------------------------------------------------------------- | ------------------------------------------------------------------- |
| **E201**              | Payment Gateway Timeout                    | Slow network, gateway overload, or dropped connection          | Check internet speed; restart terminal; check gateway status        |
| **E202**              | Merchant Authentication Failure            | Invalid credentials, account lock, or failed SSL/TLS handshake | Verify merchant account status; confirm POS has latest gateway cert |
| **E409**              | Terminal Communication Failure             | Terminal cannot reach payment processor; cable/network issue   | Reseat network/USB cables; ping payment server from network         |
| **DECLINED-INTERNAL** | Card issuer declined; non-specific decline | Card expired, insufficient funds, fraud flag, or CVV mismatch  | Customer to contact card issuer; try alternate payment method       |

### Step 6: Test Payment Gateway Connection

1. On the POS terminal, navigate to **Settings > Diagnostics > Payment Terminal Test**.
2. Select **Run Connection Test**.
3. Observe output for 30–45 seconds.
   - **Success**: "Connection Test Passed. Gateway responding." → Error is intermittent; proceed to Step 7.
   - **Failure**: "Connection Test Failed. No response from gateway." → Escalate to L2 (see "When to Escalate" section).

### Step 7: Restart the Payment Terminal

1. Gracefully power down the payment terminal (do **not** force shutdown):
   - Press **Settings > Power Options > Shutdown** on terminal screen.
   - Wait for terminal to fully power off (10–15 seconds).
2. Power terminal back on; wait for startup sequence (2–3 minutes).
3. Confirm "Ready" status displays and terminal re-syncs with POS.
4. Attempt a test transaction with a known working card.

---

## L1 Resolution

### Resolution 1: Network/Cable Reconnection (Error E409)

1. Power down the payment terminal via **Settings > Power Options > Shutdown**.
2. Inspect all cables connecting the terminal to the POS unit and network:
   - Reseat **USB/Ethernet cable** at both terminal and POS ends.
   - If using WiFi terminal, confirm SSID connection in **Settings > Network > WiFi > Connected Network**. Signal strength should show ≥3 bars.
3. Power terminal back on and wait 3 minutes for reconnection.
4. Perform test transaction.

**Expected outcome**: E409 errors resolve; transactions process normally.

---

### Resolution 2: Payment Gateway Certificate Refresh (Error E202)

1. Access the POS back-office with **manager credentials**.
2. Navigate to **System > Administration > Payment Gateway Settings**.
3. Locate **SSL Certificate** section.
4. If certificate shows "Expired" or warning icon, select **Refresh Certificate** button.
5. A dialog will prompt: "Update SSL certificates from payment gateway?" Click **Yes**.
6. System will contact gateway; wait for completion message (1–2 minutes).
7. Restart the POS terminal (via Settings > Power Options).
8. Test with a transaction.

**Expected outcome**: E202 errors resolve; authentication succeeds.

---

### Resolution 3: Clear Payment Terminal Buffer/Cache

1. On the payment terminal, press **Settings > System > Clear Transaction Buffer**.
2. Confirm the prompt: "Clear unprocessed transactions?"
3. Terminal will display "Clearing..." and restart automatically (2–3 minutes).
4. Once terminal displays "Ready," perform a test transaction.

**Expected outcome**: Orphaned transactions cleared; new transactions process.

---

### Resolution 4: Reduce Transaction Timeout Window (E201 – Intermittent Gateway)

1. Access POS back-office → **System > Administration > Payment Settings**.
2. Locate **Transaction Timeout (seconds)** setting (default: 60 seconds).
3. If E201 errors occur on slow internet, do **not** reduce timeout below 45 seconds; instead, escalate to check ISP/network quality.
4. If transactions consistently timeout despite adequate timeout setting, escalate to L2.

**Expected outcome**: Transactions have adequate time to complete on slow connections.

---

### Resolution 5: Restart POS Application (System-Wide Issue)

1. On the POS unit, log out of FoodTech POS (use manager PIN).
2. From the home screen, select **Settings > Application > Restart FoodTech POS**.
3. Confirm prompt; application will close and restart (2–3 minutes).
4. Log back in with manager credentials.
5. Perform test transaction.

**Expected outcome**: Application refreshes gateway connection; payment processing resumes.

---

## When to Escalate to L2

Escalate immediately to L2 if **any** of the following criteria are met:

### Escalation Criteria

1. **Multiple Terminals Affected**
   - Payment failures occurring on 2 or more terminals at the same location simultaneously.
   - Indicates location-wide network, gateway, or merchant account issue.

2. **Connection Test Fails Persistently** (Step 6)
   - Terminal **cannot reach payment gateway** after restart and cable reseating.
   - Error code E409 persists after L1 troubleshooting.

3. **Merchant Account Flagged or Suspended**
   - POS back-office shows **Account Status: Suspended**, **Locked**, or **Requires Attention**.
   - Back-office Payment Processing status shows red indicator for >10 minutes.

4. **Certificate Refresh Fails** (Resolution 2)
   - Refresh Certificate button returns error or times out.
   - POS displays: "Unable to contact payment gateway for certificate update."

5. **E202 Persists After Certificate Refresh**
   - Merchant authentication failure continues despite completed certificate refresh.
   - Indicates possible credentials mismatch or account-level issue.

6. **Transaction Timeout Window at Maximum (60 seconds) with Continued E201 Errors**
   - Timeouts occur despite adequate timeout setting and normal network conditions.
   - Indicates gateway-side processing delays or capacity issue.

7. **Hardware Failure Suspected**
   - Card reader is physically stuck, cracked, or unresponsive even after restart.
   - Terminal displays persistent error lights (flashing red) after full power cycle.

### Information to Collect Before Escalating

Prepare the following before contacting L2:

- **Location name** and **Store ID**
- **Terminal ID(s)** affected (visible in Settings > System Status)
- **Error code(s)** and **timestamp(s)** of most recent failures
- **FoodTech POS version** (Settings > About > Version)
- **Payment terminal model(s)** (e.g., Ingenico iCT220) and **firmware version**
- **Number of terminals affected** (1 vs. multiple)
- **Customer card type(s)** (Visa, Mastercard, Amex, Debit, etc.)
- **Results of Steps 1–6 diagnostics** (terminal status, gateway status, connection test output)
- **Screenshot(s) of error message** if possible
- **Internet speed test result** (if E201 is occurring; use fast.com or speedtest.net)
- **Merchant account status** from back-office Payment Processing page
- **Last successful transaction timestamp**

---

## Related Runbooks

- `Ingenico_Terminal_Hardware_Troubleshooting.md`
- `Verifone_Terminal_Hardware_Troubleshooting.md`
- `FoodTech_POS_Network_Connectivity.md`
- `Payment_Gateway_Account_Management.md`
- `POS_Back_Office_Login_and_Navigation.md`
- `Certificate_and_SSL_Troubleshooting.md`
- `ServeWell_Payment_Gateway_Status_and_Monitoring.md`

---

## Revision History

| Version | Date       | Notes                                                                                                        |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------ |
| 1.2     | 2025-09-15 | Updated error code decision tree; added E409 specific guidance; clarified multi-terminal escalation criteria |
| 1.1     | 2024-12-10 | Expanded Resolution 2 (certificate refresh); added network diagnostics for E201                              |
| 1.0     | 2024-06-01 | Initial version; covers FoodTech v4.2.x and v5.1.x with Ingenico/Verifone terminals                          |
