# Online Orders Sync Failure

## Overview

Orders placed through the ServeWell Online Portal (web or mobile app) are not appearing in the Point-of-Sale (POS) system, or sync errors are displaying in the portal admin dashboard. This runbook addresses webhook failures, sync delays, and diagnostic procedures for ServeWell Online Portal v3.2 and v3.4.

## Affected Systems

- **ServeWell Online Portal v3.2** (legacy; extended support)
- **ServeWell Online Portal v3.4** (current release)
- **ServeWell POS Integration Module**
- **Third-party integrations**: Zomato, Swiggy, UberEats (where applicable)
- **Webhook delivery system** (ServeWell backend)

## Symptoms

- Customer orders placed on web or mobile app do not appear in store POS within expected timeframe (2–5 minutes)
- Portal admin dashboard displays "Sync Error" or "Webhook Failed" notifications
- Orders show as "Pending" in online portal but never transition to "Confirmed" status
- POS system shows no corresponding order records
- v3.2 only: Zomato orders delayed up to 90 seconds (known behavior)
- Multiple orders affected simultaneously or intermittently
- "Connection Timeout" or "504 Gateway Error" messages in portal logs

## Immediate Steps (First 2 Minutes)

**Store staff should perform these checks before contacting IT:**

1. **Check ServeWell Portal Status Page**
   - Navigate to https://status.servewell.io in a web browser
   - Confirm "Online Orders" service shows "Operational" (green status)
   - If status shows "Degraded" or "Outage," inform customer of known issue; no immediate troubleshooting needed

2. **Verify Store is Online**
   - Confirm the store's internet connection is active (test by loading any external website)
   - Check that store WiFi/Ethernet cable is physically connected to POS terminal

3. **Check POS System Status**
   - Ensure POS terminal is powered on and fully booted
   - Confirm POS application (ServeWell POS v5.x or later) is running without error dialogs
   - Note any red warning indicators on dashboard

4. **Wait 2–3 Minutes for v3.2 Zomato Orders**
   - If orders are from Zomato aggregator on v3.2, delays up to 90 seconds are normal; wait before escalating

## L1 Diagnosis Steps

### Step 1: Verify System Version and Recent Changes

1. Open **ServeWell Online Portal Admin Dashboard** (https://admin.servewell.io)
2. Log in with your L1 support credentials
3. Navigate to **Settings > System Information**
4. Confirm the installed version:
   - Look for "Portal Version: 3.2.x" or "Portal Version: 3.4.x"
   - Note the exact build number (e.g., 3.4.2-build.447)
5. Navigate to **Settings > Sync Configuration**
6. Verify **"Auto-sync Status"** toggle is **enabled** (should be blue/ON)
7. Record the **Last Successful Sync** timestamp

### Step 2: Check Webhook Delivery Logs

1. From Admin Dashboard, navigate to **Integration > Webhooks**
2. Locate the **POS Integration Webhook** entry
3. Click **View Logs** on the right side
4. Review the last 10 webhook events:
   - **Green checkmark**: Successful delivery
   - **Red X**: Failed delivery
   - **Yellow clock**: Pending retry
5. Note the exact error message if visible (e.g., "Connection refused," "HTTP 500," "Timeout after 30s")
6. Check the **Retry Status** column—ServeWell automatically retries failed webhooks up to 3 times over 15 minutes

### Step 3: Verify POS Connection

1. In Admin Dashboard, navigate to **Integration > Connected Stores**
2. Locate the affected store in the list
3. Check the **Connection Status** indicator:
   - **Green**: POS is actively connected
   - **Yellow**: POS connection is stale (last ping >5 min ago)
   - **Red**: POS is offline
4. Click the store name to open **Store Details**
5. Note the **Last Heartbeat** timestamp (should be within last 60 seconds)
6. Record the **POS System IP Address** and **API Key Status**

### Step 4: Check for Known Service Issues

1. Return to https://status.servewell.io
2. Review **Incidents** section for any active or recent issues
3. Check the **v3.2 Known Issues** or **v3.4 Known Issues** section:
   - v3.2: Zomato sync delays (up to 90s) are expected behavior
   - v3.4: Check for any posted bugs affecting sync
4. Record any relevant incident IDs or maintenance windows

### Step 5: Test Manual Sync

1. In Admin Dashboard, navigate to **Integration > Sync Configuration**
2. Click **Manual Sync Now** button (blue button, bottom right)
3. Wait for the operation to complete (typically 10–30 seconds)
4. Confirm success message: "Sync completed successfully. X orders processed."
5. If an error appears, note the exact error message and timestamp

### Step 6: Review Order Status in Portal

1. Navigate to **Orders > All Orders** in Admin Dashboard
2. Filter by **Date** = today and **Status** = "Pending"
3. Identify the affected order(s) by order number and timestamp
4. Click on the order to open **Order Details**
5. In the **Order Timeline** section, record:
   - When order was received by portal
   - Any error messages in the timeline
   - Current status and last update timestamp
6. Verify the **Destination POS System** is correctly set (should match the store's POS)

## L1 Resolution

### Resolution Path 1: POS Connection Issue (Most Common)

**Applies when:** POS Connection Status is Yellow or Red, or Last Heartbeat is >5 minutes old

1. Contact the store and ask the manager to:
   - Restart the POS terminal (full power-off, wait 30 seconds, power-on)
   - Wait 2 minutes for POS to fully boot and reconnect
2. Return to Admin Dashboard > **Integration > Connected Stores**
3. Refresh the page (Ctrl+R or Cmd+R)
4. Confirm **Connection Status** is now Green
5. Ask the manager to resubmit a test order through the online portal
6. Wait 3 minutes and verify the test order appears in POS
7. If resolved, document the case and close

### Resolution Path 2: Manual Sync Resolves the Issue

**Applies when:** Manual Sync succeeds and stuck orders appear in POS

1. After clicking **Manual Sync Now** and seeing success message, wait 2 minutes
2. Confirm with store staff that missing orders now appear in POS
3. If orders have appeared, the issue was a temporary sync delay
4. Document in case notes: "Manual sync resolved sync delay; orders now synced"
5. Close the ticket
6. **Note:** If this occurs more than once per week, flag for L2 investigation of sync scheduler

### Resolution Path 3: Retry Webhook Delivery

**Applies when:** Webhook logs show failed deliveries (Red X) but POS is online

1. In Admin Dashboard, navigate to **Integration > Webhooks**
2. Locate the failed webhook entry in the logs
3. Click **Retry Delivery** button (if available)
4. Wait for the retry to complete
5. Refresh logs and confirm status changed to green checkmark
6. Wait 2 minutes and ask store to confirm order appears in POS
7. If successful, case resolved; document that manual retry was required

### Resolution Path 4: v3.2 Zomato Sync Delay (Expected Behavior)

**Applies to:** v3.2 only, Zomato orders, delays up to 90 seconds

1. Confirm the affected order is from Zomato (check Order Details > **Source**)
2. Confirm system version is v3.2.x
3. Inform the customer/store: "Zomato order delays up to 90 seconds are normal on v3.2. Order will sync automatically."
4. Wait the full 90 seconds, then refresh POS
5. If order appears after 90 seconds, close the ticket as resolved
6. If order does not appear after 90 seconds, escalate to L2 with note: "Zomato order exceeded normal 90s delay on v3.2"

### Resolution Path 5: Clear Browser Cache (Portal Access Issues)

**Applies when:** Portal shows old/cached order data or sync button unresponsive

1. Ask the store staff member (or perform if remote access available):
   - Clear browser cache and cookies (Ctrl+Shift+Delete or Cmd+Shift+Delete)
   - Close all ServeWell Portal browser tabs
   - Close and reopen the browser
   - Log back into Admin Dashboard
2. Return to **Integration > Sync Configuration** and retry **Manual Sync Now**
3. If issue resolved, document as "Browser cache cleared; sync restored"

## When to Escalate to L2

**Escalate immediately if ANY of the following criteria are met:**

- **Orders lost for >30 minutes:** Order placed and confirmed on portal, but never appeared in POS after 30+ minutes with no webhook errors
- **Persistent POS Connection Failure:** POS connection remains Red/offline after 2 restart attempts and 10 minutes
- **Repeated Manual Sync Required:** Manual sync required more than once per week for the same store
- **Webhook Endpoint Error:** Webhook logs show repeated "Connection refused" or "HTTP 500" errors for >1 hour
- **Database Sync Mismatch:** Admin Dashboard shows order in portal, but POS system has no record, and manual sync doesn't resolve
- **v3.4 Specific Errors:** Any error message containing "authentication failed," "invalid API key," or "webhook signature invalid"
- **Multiple Stores Affected:** 3 or more stores simultaneously experiencing sync failures (indicates service-level issue)
- **Suspected Data Loss:** Customer or store reports missing orders that cannot be located in any system

### Information to Collect Before Escalating

Compile the following in a summary before transferring to L2:

- **Affected Store Name & ID**
- **Order Number(s) and exact timestamp(s)**
- **System Version** (v3.2.x or v3.4.x with build number)
- **Order Source** (web, iOS app, Android app, Zomato, Swiggy, etc.)
- **Last Successful Sync time** (from Step 1)
- **POS Connection Status** and Last Heartbeat timestamp
- **Webhook Error Message** (exact text from logs)
- **Manual Sync Result** (success or error message)
- **Steps Already Attempted** (which resolution paths were tried)
- **Timeline** (when issue started, how long ongoing, is it intermittent or continuous)
- **Store's Internet Connection Status** (confirmed working?)

**Escalation Template:**

```
L2 Escalation: Online Orders Sync Failure
Store: [Name/ID]
Order #: [Number] | Timestamp: [Date/Time]
Portal Version: [3.2.x or 3.4.x]
POS Status: [Green/Yellow/Red] | Last Heartbeat: [Time]
Error: [Exact error message or "No error shown"]
Steps Tried: [Path 1, Path 3, etc.]
Resolution: Not resolved after L1 troubleshooting
Priority: [High if >30min, Standard otherwise]
```

## Related Runbooks

- `POS-Connection-Troubleshooting.md`
- `Webhook-Integration-Errors.md`
- `ServeWell-Portal-Admin-Login-Issues.md`
- `App-Web-Portal-Connectivity.md`
- `Store-Internet-Connectivity-Check.md`
- `Zomato-Swiggy-Integration-Sync.md`
- `L2-Database-Sync-Verification.md`

## Revision History

| Version | Date       | Notes                                                                                         |
| ------- | ---------- | --------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for v3.4 release; clarified Zomato v3.2 known delays; added escalation data checklist |
| 1.1     | 2025-03-10 | Added webhook retry mechanism; expanded POS connection diagnostics                            |
| 1.0     | 2024-06-01 | Initial version for v3.2 support                                                              |

---

**Document Owner:** ServeWell Hospitality IT Help Desk  
**Last Updated:** 2025-09-15  
**Next Review Date:** 2025-12-15
