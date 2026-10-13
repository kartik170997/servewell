# VPN Connectivity Issues

## Overview

This runbook addresses corporate VPN connectivity failures affecting remote POS management, online order integrations, and remote system access on NetLink NL-3000 v2.x devices. VPN disruptions prevent critical business operations at remote locations and require prompt diagnosis and resolution.

## Affected Systems

- **NetLink NL-3000 v2.1** through **v2.8** (all variants)
- **IPsec VPN Gateway**: NetLink Secure Connect v3.x
- **Dependent Systems**:
  - Remote POS Management Console (requires VPN tunnel)
  - Online Order Integration Module (OIM v4.2+)
  - Mobile Device Management (MDM) for kitchen displays
  - Remote Diagnostics Portal

## Symptoms

- VPN connection fails to establish; status shows "Disconnected" or "Error"
- Error codes appearing in VPN logs: **0x8001**, **0x8003**, **0x8007**, **0x8009**
- Remote POS management inaccessible; "VPN tunnel unavailable" message displayed
- Online order integrations timing out; orders not syncing to POS
- Unable to access remote management dashboard from corporate office
- VPN icon in system tray shows red "X" or yellow warning triangle
- Intermittent VPN drops every 5-15 minutes despite successful initial connection
- "Authentication failed" or "Pre-shared key mismatch" errors in Event Viewer

## Immediate Steps (First 2 Minutes)

1. **Verify internet connectivity**: Have store staff check if other internet-dependent services (web browsing, email) are working. If internet is down site-wide, this is a network issue, not VPN-specific.

2. **Check VPN status indicator**: Locate the NetLink VPN status icon in the system taskbar (bottom right). Note the current status (Connected, Disconnected, Connecting, Error).

3. **Attempt manual VPN reconnect**: Have staff right-click the VPN icon and select **"Disconnect"**, wait 10 seconds, then select **"Connect"**. Allow up to 30 seconds for connection to establish. Note if connection succeeds or what error appears.

---

## L1 Diagnosis Steps

### Step 1: Verify Basic Network Connectivity

1. Open **Command Prompt** as Administrator (right-click → Run as Administrator)
2. Execute: `ping 8.8.8.8`
3. **Expected result**: Four successful ping responses with <200ms latency
4. **If failed**: Internet connectivity issue. Escalate to network team; VPN cannot function without internet.

### Step 2: Check VPN Service Status

1. Open **Services** (type `services.msc` in Windows search)
2. Locate **"NetLink VPN Service"** in the list
3. Verify **Status** column shows **"Running"**
   - If **Stopped**: Right-click → **Start** → Wait 15 seconds for service to initialize
   - If **Disabled**: Right-click → **Properties** → Set **Startup type** to **"Automatic"** → Click **Start**
4. Document the service state in your ticket notes

### Step 3: Review VPN Connection Properties

1. Open **NetLink VPN Client** application (desktop shortcut or Start Menu)
2. Navigate to **Settings** (gear icon, bottom left)
3. Click **"Connection Profile"** tab
4. Verify the following fields match the store's assigned configuration:
   - **VPN Gateway Address**: Should be `vpn.servewell.net` (not an IP address)
   - **VPN Profile Name**: Should match store location code (e.g., `STORE-0847`, `STORE-1203`)
   - **Connection Type**: Should display **"IPsec (IKEv2)"**
5. If any field appears incorrect or blank, **do not modify**—note discrepancy and escalate to L2
6. Click **"OK"** to close without making changes

### Step 4: Attempt Service Restart (L1 Authority Only)

1. Open **Services** again (type `services.msc`)
2. Right-click **"NetLink VPN Service"** → **Restart**
3. Wait 30 seconds for service to fully restart
4. Return to **NetLink VPN Client** and observe status indicator
5. Attempt connection by clicking the **"Connect"** button (green play icon)
6. Allow up to 45 seconds for connection attempt
7. **If successful**: Document timestamp and close ticket with resolution notes
8. **If unsuccessful**: Proceed to Step 5

### Step 5: Check VPN Event Logs

1. Open **Event Viewer** (type `eventvwr.msc` in Windows search)
2. Navigate to: **Windows Logs** → **System**
3. Look for entries from **"NetLink VPN Service"** from the last 15 minutes
4. Note the **Event ID** and full error message text:
   - **Event ID 1001** = Service start failure
   - **Event ID 1003** = Connection timeout
   - **Event ID 1007** = Authentication failure
   - **Event ID 1009** = Configuration error
5. **Copy the complete error message** (right-click → Copy) for escalation
6. Also check **Applications and Services Logs** → **NetLink** folder if present
7. Screenshot any error entries with visible timestamps and error codes

### Step 6: Verify Firewall Rules

1. Open **Windows Defender Firewall with Advanced Security** (type `wf.msc`)
2. Click **"Inbound Rules"** (left panel)
3. Look for a rule named **"NetLink VPN Service"** with status **"Enabled"**
   - If present and Enabled: Firewall rules are correct
   - If missing or Disabled: **Do not modify**—escalate to L2 with note "VPN firewall rule missing/disabled"
4. Click **"Outbound Rules"** and verify a rule for **"NetLink VPN Service"** exists and is **Enabled**
5. Verify port **500 (UDP)** and **4500 (UDP)** are not blocked by checking rules containing these port numbers

---

## L1 Resolution

### Resolution Path A: VPN Service Restart (Most Common - ~60% of cases)

**Applicable when**: VPN status shows "Disconnected" but no error codes present; internet is working.

1. Open **Services** (type `services.msc`)
2. Right-click **"NetLink VPN Service"** → **Restart**
3. Wait for the service status to change to **"Running"** (may take 30 seconds)
4. Open **NetLink VPN Client** application
5. Click the **"Connect"** button (green play icon, top right)
6. Monitor the connection progress bar for up to 45 seconds
7. **If connection succeeds**:
   - Verify remote POS management and order integrations are functional
   - Document timestamp and close ticket: _"VPN service restarted; connection restored"_
   - Include any time the VPN was disconnected (useful for billing/log review)
8. **If connection fails**: Proceed to Resolution Path B

### Resolution Path B: Clear VPN Cache and Reconnect (30-40% of cases)

**Applicable when**: VPN was previously working; Error 0x8001, 0x8003, or 0x8007 appears in logs; authentication-related issues present.

1. Right-click **NetLink VPN Client** icon in system tray
2. Select **"Disconnect"** (if currently connected or attempting connection)
3. Wait 15 seconds
4. Open **File Explorer** and navigate to: `C:\Users\[USERNAME]\AppData\Local\ServeWell\NetLink`
   - Replace `[USERNAME]` with the current Windows username
   - If AppData folder is not visible: Enable "Show hidden files" (View → Hidden items checkbox)
5. Locate file: **`vpncache.dat`**
6. **Delete** `vpncache.dat` (right-click → Delete; confirm deletion)
   - Do **not** delete any other files in this folder
7. Close File Explorer
8. Return to **NetLink VPN Client** and click **"Connect"** button
9. Wait 30-45 seconds for connection
10. **If successful**: Document and close ticket with note: _"Cleared VPN cache; connection restored"_
11. **If unsuccessful**: Proceed to Resolution Path C

### Resolution Path C: Reset Network Configuration (15-20% of cases)

**Applicable when**: Multiple connection attempts fail; Network configuration may be corrupted.

1. Open **Command Prompt** as Administrator
2. Execute the following command (copy-paste exactly):
   ```
   netsh int ip reset resetlog.txt
   ```
3. Wait for command to complete (should show "Initialized successfully")
4. Execute:
   ```
   netsh winsock reset catalog
   ```
5. Wait for completion message ("successfully reset")
6. **Restart the computer** (required for changes to take effect)
   - Notify store staff that system will reboot
   - Reboot can be scheduled during non-peak hours if necessary
7. After reboot completes, log back in
8. Open **NetLink VPN Client** and attempt **"Connect"**
9. Allow 45 seconds for connection establishment
10. **If successful**: Verify all dependent systems; close ticket with note: _"Network stack reset and system rebooted; VPN connection restored"_
11. **If unsuccessful**: **Escalate to L2** with all diagnostic information collected

---

## When to Escalate to L2

**Escalate immediately if any of the following conditions are met:**

### Configuration Issues

- VPN connection properties show incorrect values (wrong Gateway address, blank Profile name)
- VPN firewall rules are missing or disabled
- Event log shows **Event ID 1007** (authentication failure) repeatedly
- Event log shows **Event ID 1009** (configuration error)

### Persistent Connection Failures After L1 Resolution Attempts

- VPN remains disconnected after service restart AND cache clear AND network reset
- Connection succeeds briefly (5-30 seconds) then drops repeatedly
- Error codes **0x8009** or **0x8003** persist in logs after multiple restart attempts

### Hardware/Device Issues

- NetLink NL-3000 device shows orange/red status LED (not green)
- VPN Client application crashes or fails to launch
- "Device not responding" message when attempting to connect

### Information to Collect Before Escalating

Gather the following in your ticket **before** handing off to L2:

1. **Store Location Code** and store name
2. **Device Serial Number** (found on NetLink device label or in NetLink VPN Client → Settings → About)
3. **NetLink Device Model and Firmware Version** (Settings → System Information)
4. **NetLink VPN Client Version** (Help → About)
5. **Complete error messages** from Event Viewer (copy full text)
6. **All attempted resolutions** with timestamps (e.g., "Service restarted 14:23 UTC; failed to connect")
7. **Screenshots** of:
   - VPN Client connection status window
   - Event Viewer error entries
   - Services status for "NetLink VPN Service"
8. **Timeline** of when issue started and how long VPN has been down
9. **Impact statement** (which systems/orders affected; business impact)

**Escalation Ticket Template:**

```
Subject: [ESCALATE L2] VPN Connectivity Failure - Store [LOCATION CODE]

L1 Diagnosis Summary:
- Issue Start Time: [TIME UTC]
- Internet Connectivity: [PASS/FAIL with details]
- VPN Service Status: [RUNNING/STOPPED/DISABLED]
- Event Log Error Code(s): [e.g., 0x8001, 1003]
- L1 Resolutions Attempted: [List with timestamps]
- Current Status: [CONNECTED/DISCONNECTED/ERROR STATE]

Affected Systems: [e.g., Remote POS, Online Orders]
Business Impact: [Brief description]

Attachments:
- Event Viewer screenshots
- VPN Client status screenshot
- Device serial number and version info
```

---

## Related Runbooks

- `netlink-nl3000-device-reset.md` — Factory reset and reconfiguration of NetLink NL-3000
- `online-order-integration-troubleshooting.md` — Resolving order sync failures
- `remote-pos-management-access.md` — Remote POS connection and authentication issues
- `windows-firewall-configuration.md` — Firewall rules and port management
- `network-connectivity-diagnostics.md` — General network troubleshooting for retail locations
- `vpn-gateway-maintenance-l2.md` — L2 reference for VPN gateway and IPsec configuration

---

## Revision History

| Version | Date       | Notes                                                                                                                                        |
| ------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for NetLink NL-3000 v2.8 release; added Event ID reference table; clarified L1/L2 escalation boundaries; added cache clear procedure |
| 1.1     | 2024-11-20 | Added firewall diagnostic step; expanded error code definitions; improved escalation template                                                |
| 1.0     | 2024-06-01 | Initial version; basic VPN restart and service diagnostics                                                                                   |

---

**Document Owner**: ServeWell IT Help Desk  
**Last Updated**: 2025-09-15  
**Next Review**: 2026-03-15
