# Aggregator Integration Disconnect (Zomato / Swiggy)

## Overview

Orders from Zomato or Swiggy are not reaching the ServeWell point-of-sale system, and the integration status displays as "Offline" or "Disconnected" in the ServeWell Online Portal v3.x. This runbook addresses the most common causes: API token expiry, aggregator-side service issues, and middleware connectivity failures.

## Affected Systems

- **ServeWell Online Portal** v3.2, v3.3, v3.4, v3.5
- **Zomato Partner App** (all current versions)
- **Swiggy Owner App** (all current versions)
- **ServeWell Aggregator Middleware** (all versions supporting Zomato/Swiggy)
- **POS Systems:** ServeWell POS Terminal v2.1+, any EPOS integrated via ServeWell API

## Symptoms

- Orders from Zomato or Swiggy do not appear in ServeWell POS or kitchen display system (KDS)
- Integration status in ServeWell Portal shows "Offline," "Connection Failed," or "Not Connected"
- Red error icon next to Zomato/Swiggy channel in Portal dashboard
- Store staff report manual order entry required for aggregator orders
- Error messages in Portal: "Authentication Failed," "Invalid API Token," or "Service Unavailable"
- Orders visible in Zomato Partner App / Swiggy Owner App but not syncing to ServeWell

## Immediate Steps (First 2 Minutes)

**These steps can be performed by store staff without IT involvement:**

1. **Verify aggregator app status:** Ask staff to open the Zomato Partner App or Swiggy Owner App on their phone/tablet. Confirm that:
   - The app loads without errors
   - They can see incoming orders in the aggregator app
   - The store status shows as "Online" in the aggregator app

2. **Check internet connectivity:** Confirm the store's Wi-Fi or broadband connection is active and stable. Test by opening a web browser and navigating to google.com.

3. **Restart the ServeWell Portal:** Close the ServeWell Online Portal browser tab and reopen it at `https://portal.servewell.local` (or your configured domain). Wait 30 seconds for the integration status to refresh.

---

## L1 Diagnosis Steps

### Step 1: Verify Aggregator Service Status

1. Ask the customer to check the **Zomato Partner App** or **Swiggy Owner App** for any banner notifications:
   - Look for maintenance alerts, service interruptions, or API downtime notices
   - Check the app's Help section for known issues
2. If the aggregator app shows a service warning, note the message and proceed to **When to Escalate to L2** (this is outside ServeWell control)
3. If no aggregator-side notice exists, proceed to Step 2

### Step 2: Check ServeWell Portal Integration Status

1. Log into **ServeWell Online Portal v3.x** with admin or manager credentials
2. Navigate to **Settings > Integrations** (or **Channel Management**, depending on v3.x variant)
3. Locate the **Zomato** or **Swiggy** integration tile
4. Record the exact status and any error message displayed:
   - **Status values to note:** "Online," "Offline," "Error," "Expired Token," "Pending Authentication"
   - **Error codes to record:** "ERR_AUTH_FAILED," "ERR_TOKEN_EXPIRED," "ERR_API_UNREACHABLE," "ERR_WEBHOOK_TIMEOUT"
5. If status is "Offline" or "Error," proceed to Step 3
6. If status is "Online," proceed to **Step 5: Check Webhook Delivery**

### Step 3: Verify API Token Expiry

1. In ServeWell Portal, navigate to **Settings > Integrations > [Zomato/Swiggy] > Details**
2. Look for a field labeled **"Token Expiry"** or **"Auth Expires On"**
3. Compare the expiry date with today's date:
   - **If expired or expiring within 7 days:** Proceed to **L1 Resolution: Step 1 (Re-authenticate)**
   - **If token shows as valid:** Proceed to Step 4

### Step 4: Check Middleware Connection Logs

1. In ServeWell Portal, navigate to **Settings > Integrations > [Zomato/Swiggy] > Connection Logs** (if available in v3.x)
2. Review the most recent log entries (last 5-10 entries)
3. Look for the following:
   - **"Successfully connected"** → Integration is functional; proceed to Step 5
   - **"HTTP 401 Unauthorized"** → Token authentication failure; proceed to **L1 Resolution: Step 1**
   - **"HTTP 403 Forbidden"** → Insufficient API permissions; proceed to **L1 Resolution: Step 2**
   - **"Connection timeout"** or **"Service unavailable (503)"** → Aggregator API may be down; proceed to **When to Escalate to L2**
   - **"Webhook delivery failed"** or **"Order callback failed"** → Proceed to Step 5

### Step 5: Check Webhook Delivery Configuration

1. Navigate to **Settings > Integrations > [Zomato/Swiggy] > Webhook Settings** (if exposed in Portal)
2. Verify that **Webhook URL** is present and formatted correctly:
   - **Expected format:** `https://[your-servewell-domain]/api/aggregators/[zomato|swiggy]/webhook`
   - **Example:** `https://portal.myrestaurant.com/api/aggregators/zomato/webhook`
3. If the Webhook URL is blank or malformed, note this for escalation to L2
4. Ask the customer if the store's firewall recently changed or if IT has deployed new network rules
5. If all webhook details appear correct, proceed to **When to Escalate to L2** with findings from Steps 1-5

---

## L1 Resolution

### Resolution Path A: API Token Expiration (Most Common)

**Use this path if Step 3 revealed an expired or expiring token.**

#### Zomato Re-authentication

1. In ServeWell Portal, navigate to **Settings > Integrations > Zomato**
2. Click the **"Re-authenticate"** or **"Reconnect"** button (red/orange button, typically top-right of the Zomato tile)
3. A popup window or new tab will open redirecting to Zomato Partner Portal login
4. Log in with the **Restaurant Partner Account** (email and password used to manage the Zomato store)
5. On the Zomato consent screen, review permissions and click **"Authorize"** or **"Allow"**
6. You will be redirected back to ServeWell Portal; wait for the confirmation message: **"Zomato integration successfully authorized"**
7. The integration status should now display as **"Online"** (may take 30-60 seconds to update)
8. Test: Ask staff to place a test order through Zomato and verify it appears in ServeWell POS within 60 seconds

#### Swiggy Re-authentication

1. In ServeWell Portal, navigate to **Settings > Integrations > Swiggy**
2. Click the **"Re-authenticate"** or **"Reconnect"** button
3. A popup window or new tab will open redirecting to Swiggy Owner Portal login
4. Log in with the **Restaurant Owner Account** (email and password used to manage the Swiggy store)
5. On the Swiggy consent screen, review permissions and click **"Allow Access"** or **"Authorize"**
6. You will be redirected back to ServeWell Portal; wait for the confirmation message: **"Swiggy integration successfully authorized"**
7. The integration status should now display as **"Online"** (may take 30-60 seconds to update)
8. Test: Ask staff to place a test order through Swiggy and verify it appears in ServeWell POS within 60 seconds

**Resolution Complete If:** Integration status is "Online" and test order appears in POS. Inform the customer that all previous pending orders may not sync; they should check the aggregator app manually for any missed orders.

---

### Resolution Path B: Insufficient API Permissions

**Use this path if Step 4 revealed "HTTP 403 Forbidden" errors.**

1. Inform the customer that the API token may have been revoked or permissions were reduced on the aggregator platform
2. Proceed with **Resolution Path A (Re-authentication)** above for the respective platform
3. During the re-authentication consent screen, ensure the restaurant account has the following permissions:
   - **Zomato:** "Order Management," "Store Settings," "API Access"
   - **Swiggy:** "Order Management," "Store Configuration," "API Integration"
4. If the consent screen does not display these permissions, the account may have insufficient role privileges; escalate to L2 with the account email address

---

### Resolution Path C: Test Order Verification (If Status Shows Online but Orders Not Arriving)

**Use this path if Step 5 determined webhook configuration is correct but orders still not syncing.**

1. Ask the customer to open the **Zomato Partner App** or **Swiggy Owner App** on a personal device
2. In the aggregator app, place a small test order (or ask IT to create a test order in the aggregator's staging environment if available)
3. Confirm the order appears in the aggregator app immediately
4. Check ServeWell POS at the store:
   - **If order appears:** Integration is working; previous orders may have been missed due to the earlier disconnect. No further action needed.
   - **If order does not appear within 2 minutes:** Proceed to **When to Escalate to L2** and include the test order ID

---

## When to Escalate to L2

**Escalate to L2 Technical Support if any of the following conditions apply:**

### Escalation Criteria

- ✓ Integration status remains "Offline" after re-authentication has been completed and 10 minutes have elapsed
- ✓ Connection logs show repeating "Service unavailable (503)" or "Connection timeout" errors for more than 30 minutes
- ✓ Webhook URL is blank, malformed, or shows as "Not Configured" in Portal (indicates a middleware deployment issue)
- ✓ Error message "HTTP 403 Forbidden" persists after re-authentication
- ✓ Store's internet connectivity is verified as good, but ServeWell Portal cannot reach the aggregator API
- ✓ Test order placed in aggregator app does not appear in ServeWell POS after 5 minutes
- ✓ Customer reports that integration was working, then suddenly stopped without any changes to store settings (potential API deprecation or aggregator-side schema change)
- ✓ ServeWell Portal shows a red banner message: "Aggregator API Maintenance Window" or "Service Unavailable"

### Information to Collect Before Escalating

Gather the following information and include in the escalation ticket:

| Information                    | Where to Find                                | Notes                                                        |
| ------------------------------ | -------------------------------------------- | ------------------------------------------------------------ |
| **Store Name & ID**            | ServeWell Portal dashboard                   | Include 6-digit store ID if visible                          |
| **Affected Aggregator(s)**     | Settings > Integrations                      | Zomato, Swiggy, or both                                      |
| **Current Integration Status** | Settings > Integrations > [Platform] Details | Exact status text and any error codes                        |
| **Token Expiry Date**          | Settings > Integrations > [Platform] Details | Record the date shown, or "Not Displayed"                    |
| **Recent Error Messages**      | Connection Logs (Settings > Integrations)    | Copy the last 5 error messages, including timestamps         |
| **Last Successful Order**      | POS history or aggregator app                | Date and time the last order synced successfully             |
| **Test Order ID**              | Create via aggregator app                    | Place a test order and capture the order number for tracking |
| **ServeWell Portal Version**   | Portal footer or Help > About                | Record exact version (e.g., v3.4.2)                          |
| **Middleware Version**         | Ask customer IT or check System Info         | If accessible to customer                                    |
| **Store Internet Type**        | Ask customer                                 | Wi-Fi, broadband, mobile hotspot, etc.                       |
| **Firewall Changes**           | Ask customer                                 | Any recent network changes, new VPN, or security updates?    |

---

## Related Runbooks

- `aggregator-test-orders-not-printing.md` — Orders visible in Portal but not printing at POS
- `servewell-portal-login-issues.md` — Troubleshooting Portal authentication and access
- `internet-connectivity-diagnostics.md` — Testing store network connectivity
- `servewell-pos-offline-recovery.md` — Recovering POS when disconnected from Portal
- `zomato-api-account-setup.md` — Initial Zomato integration configuration
- `swiggy-api-account-setup.md` — Initial Swiggy integration configuration
- `aggregator-webhook-debugging.md` — Advanced webhook payload inspection (L2)
- `middleware-service-restart.md` — Restarting aggregator middleware components (L2)

---

## Revision History

| Version | Date       | Notes                                                                                          |
| ------- | ---------- | ---------------------------------------------------------------------------------------------- |
| 1.3     | 2025-09-15 | Added Step 5 (webhook verification), expanded escalation criteria, added test order procedures |
| 1.2     | 2025-06-20 | Clarified re-auth steps for both platforms, added specific error codes                         |
| 1.1     | 2025-03-10 | Refined immediate steps for store staff, added version numbers                                 |
| 1.0     | 2024-12-01 | Initial runbook creation                                                                       |

---

## Appendix: Quick Reference - Common Error Codes

| Error Code                     | Meaning                                    | L1 Action                                             |
| ------------------------------ | ------------------------------------------ | ----------------------------------------------------- |
| `ERR_TOKEN_EXPIRED`            | API authentication token has expired       | Re-authenticate (Resolution Path A)                   |
| `ERR_AUTH_FAILED`              | Token is invalid or revoked                | Re-authenticate (Resolution Path A)                   |
| `ERR_API_UNREACHABLE`          | Cannot contact aggregator API servers      | Check internet; escalate if persists >30 min          |
| `HTTP 401 Unauthorized`        | Missing or invalid API credentials         | Re-authenticate (Resolution Path A)                   |
| `HTTP 403 Forbidden`           | Insufficient API permissions on account    | Re-authenticate & verify permissions (Path B)         |
| `HTTP 503 Service Unavailable` | Aggregator API under maintenance           | Verify status via aggregator app; escalate if ongoing |
| `ERR_WEBHOOK_TIMEOUT`          | Order callback not received within timeout | Escalate to L2 for webhook debugging                  |
| `ERR_WEBHOOK_FAILED`           | Order notification could not be delivered  | Check store firewall/network; escalate if needed      |

---

**Document Owner:** ServeWell Hospitality IT Support  
**Last Updated:** September 15, 2025  
**Next Review Date:** December 15, 2025
