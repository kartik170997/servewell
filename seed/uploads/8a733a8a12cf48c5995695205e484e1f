# Online Orders Menu Mismatch

## Overview

The ServeWell Online Portal v3.x menu displays outdated, incorrect, or incomplete item data that does not match the restaurant's current POS or third-party delivery platform inventory. This causes customer confusion, failed orders, and revenue loss. L1 support can trigger a manual menu synchronization refresh; actual menu content corrections require L2 or portal administrator intervention.

## Affected Systems

- **ServeWell Online Portal** v3.2 and later
- **Zomato Integration Module** (API sync, all versions)
- **Swiggy Integration Module** (API sync, all versions)
- **POS System** (connection layer only)
- **Database** ServeWell_Portal_Live (menu cache tables)

## Symptoms

- Menu item prices differ between online portal and in-store POS by ≥₹10 or more
- Items marked "Out of Stock" in POS appear as "Available" in online portal
- Recently added menu items do not appear on Zomato or Swiggy listings after 2+ hours
- Customer orders placed for unavailable items (e.g., sold-out dishes)
- Third-party delivery platform shows different item count than ServeWell portal
- Seasonal or promotional items missing from one or more sales channels
- "Menu sync failed" error message in portal admin dashboard

## Immediate Steps (First 2 Minutes)

_These quick checks require no IT access and can be performed by restaurant staff:_

1. **Verify POS inventory status** – Open the in-store POS system and confirm current item availability and pricing. Note any items marked "unavailable" or "out of stock."
2. **Check third-party platforms** – Open Zomato and Swiggy apps/websites directly and compare visible menu items and prices to what customers are reporting.
3. **Note the discrepancy type** – Record whether the issue is price mismatch, availability mismatch, or missing items, and document specific examples (item name, expected price, portal price, etc.).
4. **Check internet connectivity** – Verify that the restaurant location has stable internet. A poor connection may prevent menu syncs from completing.

## L1 Diagnosis Steps

1. **Log into ServeWell Portal Admin Console**
   - Navigate to `https://portal.servewell.local/admin` (or production URL as per your environment)
   - Authenticate using your L1 support credentials
   - Confirm you have "Menu Management" role permissions

2. **Access the Menu Sync Status Dashboard**
   - From the left navigation menu, select **Settings** → **Integrations** → **Menu Sync Status**
   - Note the timestamp of the last successful sync under each platform:
     - "Last Zomato Sync:" `[timestamp]`
     - "Last Swiggy Sync:" `[timestamp]`
   - If any shows "Failed" status, record the error code (e.g., `ERR_API_401`, `ERR_TIMEOUT_30s`)

3. **Review Sync Error Log**
   - Click **View Sync Log** to expand the last 10 sync attempts
   - Look for error entries matching the time when the issue was first reported
   - Record any error messages, status codes, or API rejection reasons

4. **Cross-reference Item Discrepancies**
   - Go to **Catalog** → **Menu Items**
   - Search for the specific item(s) reported by the customer using the search bar at the top
   - Click on each item and verify:
     - **Price field** matches the in-store POS pricing (confirm with staff)
     - **Availability toggle** is set to "Active" if the item is in stock
     - **Platform sync checkboxes** – Confirm "Sync to Zomato" and "Sync to Swiggy" are checked if applicable
     - **Last Updated** timestamp (should be recent if manually edited)

5. **Check Portal Database Sync Delay**
   - If the last successful sync was >4 hours ago, this may indicate a connectivity or API issue
   - If the last sync was <30 minutes ago and discrepancies persist, the issue is likely in the POS integration layer, not the third-party platforms

6. **Verify POS Connection Status**
   - Go to **Settings** → **System Health** → **POS Connections**
   - Confirm the status shows "Connected" (green indicator)
   - If status is "Disconnected" or "Warning," this is the root cause—proceed to escalation

7. **Test Connectivity to Third-Party APIs**
   - Navigate to **Settings** → **API Status Dashboard**
   - Click **Test Connection** for Zomato and Swiggy integrations separately
   - Record the response:
     - ✓ "Connection successful" = API is reachable
     - ✗ "Connection timeout" = Network/firewall issue
     - ✗ "Authentication failed (401/403)" = API credentials issue

## L1 Resolution

### **Scenario A: Menu Sync Is Stale (>4 Hours Since Last Sync)**

1. Go to **Settings** → **Integrations** → **Menu Sync Status**
2. Click the **Force Menu Refresh** button next to the affected platform (Zomato or Swiggy)
3. A confirmation dialog will appear: "This will immediately sync menu data. Continue?"
4. Click **Confirm**
5. Monitor the status indicator. You will see:
   - "Syncing..." (spinning icon) for 30–90 seconds
   - "Sync completed successfully" (green) = issue resolved, OR
   - "Sync failed: [error code]" (red) = escalate to L2 with error code
6. If successful, instruct the customer to refresh their browser or mobile app (clear cache if needed) and verify the menu now shows correct data

### **Scenario B: Item Availability Toggle Is Incorrect**

1. Go to **Catalog** → **Menu Items**
2. Search for the problematic item by name
3. Click the item to open its details page
4. Check the **Availability Status** toggle at the top:
   - If set to "Inactive" but should be "Active": Click the toggle to activate
   - If set to "Active" but should be "Inactive": Click the toggle to deactivate
5. Scroll down and verify the **Sync Platforms** section:
   - Ensure "Sync to Zomato" and "Sync to Swiggy" checkboxes match the restaurant's policy
6. Click **Save Changes** at the bottom
7. Return to **Menu Sync Status** and click **Force Menu Refresh** for each platform
8. Confirm both syncs complete successfully before closing the ticket

### **Scenario C: Item Price Mismatch**

1. Verify the discrepancy is not a display error (check POS pricing first with staff)
2. **Do NOT edit the price directly in the portal** – this requires L2/admin approval
3. Document the following before escalating:
   - Item name
   - Current portal price
   - Correct POS price
   - Which platform(s) are affected (Zomato, Swiggy, or both)
   - Timestamp of when the price was last correct
4. Proceed to "When to Escalate to L2" section

### **Scenario D: Recently Added Item Not Appearing in Zomato/Swiggy**

1. Go to **Catalog** → **Menu Items** and search for the new item
2. Open the item details and confirm:
   - **Status** is set to "Active"
   - **Item Category** is assigned (e.g., "Appetizers," "Mains")
   - **Sync to Zomato** checkbox is ☑ (checked)
   - **Sync to Swiggy** checkbox is ☑ (checked)
3. If any checkbox is unchecked, check it and click **Save Changes**
4. Return to **Menu Sync Status** and click **Force Menu Refresh** for Zomato and Swiggy
5. Wait 2–3 minutes for items to appear on the respective platforms
6. If the item still does not appear after 5 minutes, escalate with details

## When to Escalate to L2

Escalate immediately to L2 support or portal administrator if any of the following conditions are true:

### **Escalation Criteria**

- **POS Connection Status** shows "Disconnected" or "Error" (system-level issue, not menu-specific)
- **API Connection Test** fails for Zomato or Swiggy with error codes `401`, `403`, or `TIMEOUT`
- **Sync Log** contains repeated errors over multiple attempts (>3 failed syncs in the last 2 hours)
- **Force Menu Refresh** button returns: `"ERR_SYNC_FATAL"`, `"ERR_DB_LOCK"`, or `"ERR_API_RATE_LIMIT"`
- **Price corrections required** – L1 agents cannot modify item prices; L2 must approve and apply pricing changes
- **Bulk item discrepancies** – More than 10 items have mismatched data across platforms
- **Third-party platform mapping issue** – Item appears in portal but is mapped to wrong category on Zomato/Swiggy (requires platform-specific admin access)
- **Database sync conflicts** – Portal displays conflicting data between two successful syncs (data integrity issue)

### **Information to Collect Before Escalating**

Create a summary document with the following details:

| Field                          | Required Information                                                        |
| ------------------------------ | --------------------------------------------------------------------------- |
| **Restaurant Name & Location** | Full legal name and address (for multi-location accounts)                   |
| **Issue Type**                 | Price mismatch / Availability mismatch / Missing items / Other              |
| **Affected Items**             | Item name, SKU, current price, expected price (if applicable)               |
| **Affected Platforms**         | Zomato / Swiggy / Both / Portal only                                        |
| **Last Successful Sync**       | Timestamp from Menu Sync Status dashboard                                   |
| **Error Code(s)**              | Exact error message(s) from sync log or API test                            |
| **POS System**                 | Model/version (e.g., "Square POS v2.1")                                     |
| **Screenshots**                | Portal screenshot showing discrepancy + POS screenshot showing correct data |
| **Customer Impact**            | Number of failed orders, revenue loss estimate if known                     |
| **Reproduction Steps**         | Step-by-step instructions for L2 to reproduce the issue                     |
| **Time Reported**              | Exact date/time issue was first discovered                                  |

**Escalation Template (to be pasted into ticket):**

```
ESCALATION TO L2 SUPPORT

Issue: [Menu Mismatch / Sync Failure / etc.]
Restaurant: [Name]
Location: [Address]
Reported at: [Date/Time UTC]

Root Cause (L1 diagnosis): [POS disconnect / Failed API sync / Incorrect toggle / Price edit required]

Affected Items:
- [Item 1]: Portal price ₹[X] vs. POS price ₹[Y]
- [Item 2]: Listed as available in portal, out of stock in POS

Last Sync Status: [Timestamp and result]
Error Code: [If applicable]

Action Required: [Menu refresh failed / Price correction needed / Database sync issue / API credential update]

Attachments: [Portal screenshot, POS screenshot, sync log export]
```

## Related Runbooks

- `POS_Integration_Connection_Troubleshooting.md`
- `Zomato_API_Authentication_Setup.md`
- `Swiggy_Integration_Sync_Configuration.md`
- `ServeWell_Portal_Admin_Access_Management.md`
- `Database_Menu_Cache_Purge_Procedure.md`
- `Third_Party_Delivery_Platform_Mapping_Guide.md`

## Revision History

| Version | Date       | Notes                                                                                                                                                                   |
| ------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for ServeWell Portal v3.2+; clarified L1 scope (sync refresh only); added API connection test procedures; revised escalation criteria with specific error codes |
| 1.1     | 2024-11-20 | Added Swiggy integration details; expanded POS connection diagnostics                                                                                                   |
| 1.0     | 2024-06-01 | Initial version; covered Zomato integration and basic menu sync procedures                                                                                              |

---

**Document Owner:** ServeWell Hospitality L2 Support Team  
**Last Reviewed:** 2025-09-15  
**Next Review Date:** 2026-03-15
