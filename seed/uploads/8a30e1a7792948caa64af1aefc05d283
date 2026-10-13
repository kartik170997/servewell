# Online Orders Not Appearing on KDS

## Overview

Orders successfully received by the ServeWell Online Portal v3.x are not displaying on the Kitchen Display System (KDS). This indicates a breakdown in the portal-to-KDS integration, typically occurring at either the portal-to-store communication layer or the store-to-KDS middleware layer.

## Affected Systems

- **ServeWell Online Portal:** v3.0 and later
- **KDS Middleware:** servewell-kds-bridge service (all versions)
- **Kitchen Display System:** All integrated models (Margin, Toast, MarginPro)
- **Network:** Store-level local area network (LAN) connectivity required

## Symptoms

- Orders appear in **Online Orders** menu on portal but not on KDS display
- Customer receives order confirmation email/SMS but kitchen staff see no ticket
- Some orders appear; others do not (intermittent behavior)
- KDS displays "No Active Orders" despite portal showing pending orders
- KDS error message: "Connection Lost" or "Middleware Unavailable"
- Portal shows order status as "Received" but KDS shows "Not Connected"

## Immediate Steps (First 2 Minutes)

**For store staff calling in:**

1. **Verify order received:** Check the **Online Orders** section in the ServeWell Portal. Navigate to **Orders > View Online Orders**. Confirm the order appears with status "Received" or "Confirmed."

2. **Check KDS display power:** Ensure the Kitchen Display System monitor is powered on and displaying the standard order queue screen (not a screensaver, error screen, or blank display).

3. **Restart the KDS system:** Power cycle the KDS terminal completely (full shutdown, wait 30 seconds, power on). Allow 2 minutes for system startup. Check if the order now appears.

---

## L1 Diagnosis Steps

### Step 1: Confirm Portal-Side Reception

1. Ask the store contact to log into the ServeWell Online Portal with manager credentials.
2. Navigate to **Orders** → **View Online Orders**.
3. Look for the order in question. Note the exact **Order ID** and **Time Received**.
4. **Expected outcome:** Order should appear with status "Received" or "Confirmed."
5. **If order NOT visible:**
   - This is a **portal reception failure**, not a KDS integration issue.
   - Refer to runbook: `Online_Orders_Not_Received_by_Portal.md`
   - **Stop here and do not proceed with KDS diagnostics.**
6. **If order IS visible:** Proceed to Step 2.

### Step 2: Check Portal-to-Store Network Connection

1. In the portal, navigate to **Admin** → **Store Settings** → **System Status**.
2. Locate the field **"Store Connection Status."**
3. **Expected display:** "Connected" (green indicator) with timestamp of last sync within the last 2 minutes.
4. **If status is "Disconnected" (red):**
   - The store location is not receiving data from the portal.
   - Document the disconnection time.
   - Proceed to Step 3.
5. **If status is "Connected":** Proceed to Step 4.

### Step 3: Verify Store Network Connectivity

1. Ask the store manager to check internet connectivity:
   - Open a browser and navigate to `www.google.com`
   - Attempt to load another cloud-based service the store uses (e.g., email, point-of-sale system).
2. **If internet is DOWN:** Network issue is outside KDS scope. Escalate to store manager to resolve ISP/firewall issues.
3. **If internet is UP:** Proceed to Step 4.

### Step 4: Check servewell-kds-bridge Service Status

1. Remote into the **store server** (the local machine hosting KDS middleware integration—typically the POS server or dedicated terminal).
   - Use RDP, SSH, or your standard remote access tool.
   - Credentials: Use store IT account or escalate to L2 for access.
2. Once connected, open **Services Manager**:
   - **Windows:** Press `Win + R`, type `services.msc`, press Enter.
   - **Linux:** Open terminal and run `sudo systemctl status servewell-kds-bridge`
3. Search for or scroll to **servewell-kds-bridge** in the Services list.
4. Check the **Status** column:
   - **Expected state:** "Running" (Windows) or "active (running)" (Linux)
   - **If status is "Stopped":** Proceed to Step 5.
   - **If status is "Running":** Proceed to Step 6.

### Step 5: Check Service Startup Logs

1. Still in Services Manager, right-click **servewell-kds-bridge** → **Properties**.
2. Note the **Startup Type** (should be "Automatic").
3. Click **Log On** tab and verify the service is running under the correct user account.
4. Check the **Dependencies** tab. Note any services that must be running first.
5. Document any error messages or unusual log entries.

### Step 6: Test KDS Middleware Connectivity

1. On the store server, open a **Command Prompt** (Windows) or **Terminal** (Linux).
2. Run the diagnostic command:
   ```
   servewell-kds-bridge --test-connection
   ```
3. **Expected output:**
   ```
   Portal Connection: OK
   KDS Device Connection: OK
   Message Queue: OK
   ```
4. **If any connection shows "FAILED":**
   - Note the exact failure message.
   - Document the failure type (Portal, KDS Device, or Message Queue).
   - Proceed to L1 Resolution Steps.
5. **If all connections show "OK":**
   - Manual integration test: Request store staff to place a test online order and observe KDS within 30 seconds.
   - If order appears: **Issue is resolved.** Document resolution time and close ticket.
   - If order still does not appear: **Escalate to L2.** See "When to Escalate to L2" section.

---

## L1 Resolution

### Resolution Path A: Restart servewell-kds-bridge Service (Most Common)

**Use this if diagnostic Step 4 showed service status as "Stopped."**

1. On the store server, open **Services Manager** (Windows: `services.msc` | Linux: terminal).
2. Right-click **servewell-kds-bridge** service → **Start**.
3. Wait 30 seconds for service to fully initialize.
4. Verify status changed to "Running" or "active (running)".
5. Ask store staff to place a test online order.
6. Observe KDS within 60 seconds. Order should appear as a new ticket.
7. **If order appears:** Service restart successful. Proceed to Step 8.
8. Document the resolution:
   - Service was stopped; restarted successfully.
   - Test order confirmed visible on KDS.
   - Close ticket with status "Resolved."

---

### Resolution Path B: Restart servewell-kds-bridge with Dependency Check

**Use this if service is running but connectivity test (Step 6) failed.**

1. Verify the dependent services are running:
   - **Windows:** In Services Manager, check status of:
     - `ServeWell Portal Agent` (should be "Running")
     - `KDS Sync Service` (should be "Running")
   - **Linux:** Run:
     ```
     sudo systemctl status servewell-portal-agent
     sudo systemctl status servewell-kds-sync
     ```
2. If any dependent service is stopped, start it first:
   - Right-click service → **Start** (Windows)
   - Or `sudo systemctl start [service-name]` (Linux)
3. Wait 1 minute for dependent services to initialize.
4. Now restart **servewell-kds-bridge**:
   - Right-click → **Restart** (Windows)
   - Or `sudo systemctl restart servewell-kds-bridge` (Linux)
5. Wait 30 seconds.
6. Re-run the diagnostic command:
   ```
   servewell-kds-bridge --test-connection
   ```
7. **If test-connection now shows "OK" for all items:**
   - Request store staff place a test order.
   - Confirm order appears on KDS within 60 seconds.
   - Close ticket as "Resolved."
8. **If test-connection still shows failures:** Escalate to L2 (see below).

---

### Resolution Path C: Clear Middleware Cache

**Use this if connectivity test passes but orders still not appearing.**

1. On the store server, navigate to the middleware cache directory:
   - **Windows:** `C:\ProgramData\ServeWell\kds-bridge\cache\`
   - **Linux:** `/var/lib/servewell/kds-bridge/cache/`
2. Delete all files in this directory (safe to remove; cache will rebuild).
3. Restart servewell-kds-bridge service:
   - Right-click **servewell-kds-bridge** → **Restart** (Windows)
   - Or `sudo systemctl restart servewell-kds-bridge` (Linux)
4. Wait 45 seconds for cache rebuild.
5. Request store staff place a fresh test online order.
6. Confirm order appears on KDS within 60 seconds.
7. **If successful:** Close ticket as "Resolved - Cache Cleared."
8. **If unsuccessful:** Proceed to "When to Escalate to L2."

---

## When to Escalate to L2

Escalate a ticket to L2 Support **immediately** if any of the following apply:

### Escalation Criteria:

1. **servewell-kds-bridge service will not start** after following Resolution Path A, and the service log shows errors other than "service stopped."
2. **Connectivity test fails persistently** (Step 6 shows "FAILED") on multiple restart attempts, with error codes such as:
   - `ERR_PORTAL_AUTH_FAILED`
   - `ERR_KDS_DEVICE_UNREACHABLE`
   - `ERR_MESSAGE_QUEUE_TIMEOUT`
3. **Portal shows order but KDS has no network connection** (Step 2 shows "Disconnected") and internet connectivity is confirmed (Step 3).
4. **Dependent services will not start** (`ServeWell Portal Agent` or `KDS Sync Service`).
5. **Orders consistently appear on portal but never on KDS** after all L1 steps and multiple test orders.
6. **Hardware failure suspected:** KDS display shows error codes, no video output, or repeated crashes.

### Information to Collect Before Escalating:

- **Ticket number:** Document for reference.
- **Store location name and ID:** Verify correct store.
- **Order ID(s):** At least one confirmed example order that failed to appear.
- **Timestamps:** When order was placed, when IT was contacted, when issue was first noticed.
- **Service status output:** Screenshot or copy/paste of full `servewell-kds-bridge --test-connection` output.
- **Recent system changes:** Ask store manager if anything was rebooted, updated, or changed in last 24 hours.
- **L1 steps completed:** List which resolution paths were attempted and their outcomes.
- **Store server details:** OS version, servewell-kds-bridge service version (run `servewell-kds-bridge --version`).
- **Error log snippet:** Copy last 20 lines from:
  - **Windows:** Event Viewer → Windows Logs → Application (filter for "ServeWell" errors)
  - **Linux:** `sudo tail -20 /var/log/servewell/kds-bridge.log`

### Escalation Format:

Submit ticket to **L2 KDS Integration Team** with subject line:

```
[ESCALATION] Online Orders Not Appearing on KDS - [Store Name] - Order ID [####]
```

Include all collected information above in the ticket body.

---

## Related Runbooks

- `Online_Orders_Not_Received_by_Portal.md` — For orders not reaching portal at all
- `KDS_Middleware_Installation_and_Setup.md` — For initial KDS integration configuration
- `Store_Server_Network_Connectivity_Troubleshooting.md` — For internet/LAN issues
- `ServeWell_Portal_Order_Status_Codes.md` — For interpreting order status meanings
- `Kitchen_Display_System_Hardware_Restart.md` — For KDS display power and connectivity resets

---

## Revision History

| Version | Date       | Notes                                                                                                    |
| ------- | ---------- | -------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated servewell-kds-bridge commands for v2.1; added cache clearing step; clarified dependent services. |
| 1.1     | 2024-12-10 | Added Linux service management procedures; expanded troubleshooting for portal-to-store layer.           |
| 1.0     | 2024-06-01 | Initial version; Windows-focused procedures.                                                             |

---

**Document Owner:** ServeWell Hospitality IT Help Desk  
**Last Updated:** 2025-09-15  
**Next Review Date:** 2026-03-15
