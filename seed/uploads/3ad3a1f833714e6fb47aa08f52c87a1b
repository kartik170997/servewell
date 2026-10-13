# Guest Wi-Fi Network Down

## Overview

This runbook addresses service interruptions affecting the ServeWell-Guest SSID while the operational network remains functional. Guest Wi-Fi outages directly impact customer experience and revenue. This guide provides L1 agents with diagnostic and resolution procedures that isolate guest network issues without affecting POS or internal operations.

## Affected Systems

- **NetLink NL-3000 v2.x** (wireless access point controller)
- **ServeWell-Guest SSID** (customer-facing broadcast)
- **Guest VLAN** (isolated network segment, typically VLAN 250)
- Dependent services: Captive portal authentication, guest bandwidth management

## Symptoms

- Customers unable to locate or connect to "ServeWell-Guest" SSID
- "Cannot connect to this network" error after password entry
- Successful connection but no internet access (stuck on captive portal)
- Connection drops intermittently or after 5–10 minutes
- Operational network (employee Wi-Fi/ethernet) functioning normally
- No alerts on POS systems or internal servers
- Multiple customer complaints within same location

## Immediate Steps (First 2 Minutes)

**Action 1: Confirm Operational Network Status**

- Ask store staff: Are POS terminals, kitchen displays, and employee devices online?
- **Result:** If operational network is down, escalate to general network outage runbook instead.

**Action 2: Test Guest Network Visibility**

- Have staff member attempt to connect to ServeWell-Guest from personal device
- Confirm SSID appears in available networks list
- Note exact error message or behavior observed

**Action 3: Check NetLink Controller Status Light**

- Locate NetLink NL-3000 unit (typically in manager office or server closet)
- Verify **Power LED is solid green** and **Status LED is blinking green**
- If LEDs are red, amber, or off → proceed to Step 1 under L1 Diagnosis

## L1 Diagnosis Steps

**Step 1: Access NetLink Web Interface**

1. Open browser on any operational network device
2. Navigate to `https://netlink-admin.local:8443` or the location's assigned admin IP (consult local setup sheet)
3. Log in with L1 support credentials (guest/guest or as configured)
4. If login fails → **Check network connectivity to controller**; ping the controller IP from an operational device

**Step 2: Verify Guest SSID Configuration**

1. In NetLink interface, navigate to **Wireless > SSID Management**
2. Locate "ServeWell-Guest" in the SSID list
3. Check the **Status** column:
   - **Active (Green):** SSID is broadcasting; proceed to Step 3
   - **Disabled (Red):** SSID has been manually disabled; proceed to Step 6
   - **Error (Orange):** Configuration fault; note error code and escalate

**Step 3: Verify Guest VLAN Assignment**

1. Click on **ServeWell-Guest** row to open configuration details
2. Under **Network Settings**, confirm:
   - VLAN ID: **250** (or location-specific guest VLAN per site documentation)
   - Bridge Mode: **Enabled**
   - Isolation Mode: **Enabled** (prevents guest access to internal network)
3. If VLAN is incorrect or shows **0** (untagged) → **escalate to L2**; this indicates controller misconfiguration

**Step 4: Check Wireless Radio Status**

1. Navigate to **Wireless > Radio Status**
2. Confirm all radio entries show:
   - **Band:** 2.4 GHz and 5 GHz (if dual-band)
   - **Transmit Power:** Normal (typically 15–20 dBm)
   - **Status:** Online/Active
3. If any radio shows **Offline** or **Error [code]** → note the error code and proceed to Step 5

**Step 5: Check Client Connection Logs**

1. Navigate to **Monitoring > Client Connections**
2. Filter by **SSID: ServeWell-Guest**
3. Observe recent connection attempts:
   - **"Auth Failed"** entries → likely password issue (Step 7)
   - **"DHCP Timeout"** entries → guest VLAN routing issue (escalate to L2)
   - **No entries in past 5 minutes** → SSID not broadcasting or clients cannot reach AP (Step 6)
4. Document the 3–5 most recent entries with timestamps for escalation if needed

**Step 6: Check NetLink System Health**

1. Navigate to **System > Health & Status**
2. Review the following metrics:
   - **CPU Usage:** Should be <70%
   - **Memory Usage:** Should be <80%
   - **Temperature:** Should be <60°C
   - **Uptime:** Note if recently rebooted (within past 30 minutes)
3. If any metric is in red → system may be throttling services; note values for escalation

## L1 Resolution

### Resolution Path A: SSID Disabled (Common)

**Symptom:** SSID status shows **Disabled (Red)** in Step 2

1. In **Wireless > SSID Management**, click **ServeWell-Guest** row
2. Locate **Enable SSID** toggle (typically at top of configuration panel)
3. Click toggle to switch from **Off** to **On**
4. Click **Save Configuration** button (blue button, bottom-right)
5. Confirm confirmation dialog appears: _"SSID changes will take effect in 10–15 seconds. Continue?"_
6. Click **Confirm**
7. **Wait 30 seconds**, then test:
   - Have store staff scan for ServeWell-Guest SSID from personal device
   - Attempt connection with known-good password
8. **Document:** Note in ticket why SSID was disabled (accidental click, scheduled maintenance, etc.)

---

### Resolution Path B: Guest VLAN DHCP Issue (Moderate)

**Symptom:** Clients connect to SSID but cannot reach internet; stuck on captive portal or "No Internet" message

1. Navigate to **Network > DHCP Management**
2. Confirm **Guest VLAN DHCP Pool** exists:
   - **VLAN ID:** 250
   - **Pool Range:** Typically 10.250.100.1–10.250.100.254 (or per site docs)
   - **Status:** Enabled
3. If DHCP pool is **Disabled**:
   - Click on the guest VLAN DHCP entry
   - Click **Enable DHCP** toggle
   - Click **Save Configuration**
   - Wait 30 seconds and test from personal device
4. If DHCP pool is **Enabled** but guests still cannot access internet:
   - Navigate to **Network > Routing**
   - Verify **Guest VLAN (250) to Internet Gateway** route exists and is **Active**
   - If route is missing or shows **Inactive** → **Escalate to L2**; routing table corruption suspected

---

### Resolution Path C: Password Issue (Very Common)

**Symptom:** Client receives "Cannot connect to this network" or "Incorrect password" message

1. Navigate to **Wireless > SSID Management**
2. Click **ServeWell-Guest** to open configuration
3. Scroll to **Security Settings** section
4. Confirm **Authentication Type:** WPA2-PSK or WPA3 (not Open)
5. Click **Show Password** option (if available) or **Edit Password** button
6. **Compare displayed password** with what store staff are using:
   - Check for case sensitivity, special characters, spaces
   - Common issue: Password changed in security audit but staff weren't notified
7. If password is incorrect or expired:
   - Click **Generate New Password** (system will create 12-character random password)
   - Note the new password in the ticket
   - Immediately communicate new password to store manager via phone call + email
   - Click **Save Configuration**
   - Wait 30 seconds and test connection
8. **Document:** Confirm date of last password change and whether store was notified

---

### Resolution Path D: Wireless Radio Offline (Less Common)

**Symptom:** In Step 4, one or more radios show **Offline** status

1. Locate the NetLink NL-3000 unit physically
2. **Hard reset procedure (does NOT affect POS network):**
   - Identify the small **Reset** button on the rear panel (recessed, requires pen/paperclip)
   - Press and hold Reset for **5 seconds** (until Status LED flashes amber)
   - Release and wait **2–3 minutes** for controller to reboot
   - Controller will retain all configurations; only wireless radios will reinitialize
3. After reboot, verify Status LED returns to **solid green**
4. Return to NetLink web interface (**Wireless > Radio Status**)
5. Confirm radios now show **Online**
6. Test guest SSID connection from personal device
7. If radios remain **Offline** after reset → **Escalate to L2 with note:** "Radio offline after reset; possible hardware failure"

---

### Resolution Path E: High System Load (Rare but Possible)

**Symptom:** CPU >75%, Memory >85%, but no obvious errors; guest network slow or intermittent

1. Navigate to **System > Running Services**
2. Review list of active services; confirm **Wireless Service**, **DHCP Service**, and **Routing Service** all show **Running**
3. If any critical service shows **Stopped**, click service name and select **Start Service**
4. Perform a controlled reboot:
   - Navigate to **System > Administration > Reboot Controller**
   - Click **Schedule Reboot in 2 Minutes** (gives time to notify staff)
   - Alert store manager: "Wireless controller is rebooting. Guest Wi-Fi will be unavailable for 3–5 minutes. POS systems unaffected."
5. Wait for controller to come back online (Status LED solid green)
6. Verify guest SSID is broadcasting and clients can connect
7. **Document:** Note CPU/memory load before reboot and current state after

---

## When to Escalate to L2

**Escalate immediately if any of the following conditions exist:**

1. **VLAN Configuration Error** (Step 3)
   - VLAN ID shows as **0** or does not match site documentation
   - Bridge Mode is **Disabled**
   - _Indicates controller misconfiguration requiring admin access_

2. **Routing Table Issues** (Resolution Path B, Step 4)
   - Guest VLAN route missing or shows **Inactive**
   - Cannot ping internet gateway from guest VLAN
   - _Indicates network infrastructure issue beyond wireless scope_

3. **DHCP Scope Exhaustion**
   - All DHCP addresses in use; clients cannot obtain IP
   - Navigate to **DHCP > Lease Status** and confirm pool is at 100% utilization
   - _Requires scope expansion or client cleanup by L2_

4. **Hardware Failure Suspected** (Resolution Path D)
   - Radios remain **Offline** after reset
   - Status LED remains red or off after power cycle
   - NetLink unit shows physical damage
   - _May require hardware replacement_

5. **Persistent DHCP/Auth Failures Despite Configuration Checks**
   - Client logs show consistent "Auth Failed" or "DHCP Timeout" errors (Step 5)
   - Resolution Paths A–E have not resolved issue
   - _Indicates deeper authentication or VLAN bridging problem_

6. **Multiple SSID Outage or Operational Network Degradation**
   - Both guest and operational networks affected simultaneously
   - _Indicates potential controller-wide failure_

### Information to Collect Before Escalating

- **Screenshot of NetLink Health & Status page** (System > Health & Status)
- **Last 10 client connection log entries** filtered by ServeWell-Guest SSID (Monitoring > Client Connections)
- **Guest SSID configuration export** (click ServeWell-Guest, screenshot Security Settings + Network Settings)
- **Exact error message** from customer device attempting to connect
- **Timestamp of issue onset** (when customers first reported problem)
- **NetLink uptime** (System > Administration > System Information)
- **Recent configuration changes** (ask store manager if anything changed in past 24 hours)

---

## Related Runbooks

- `Operational_Network_Down.md` — If POS and employee network also affected
- `Captive_Portal_Authentication_Issues.md` — If guests connect but cannot access portal login
- `NetLink_NL3000_Hardware_Replacement.md` — If hardware failure confirmed
- `Guest_Network_Bandwidth_Throttling.md` — If network is up but extremely slow
- `Wireless_Coverage_Dead_Zones.md` — If SSID broadcasts but connection is weak in certain areas
- `NetLink_Controller_Password_Reset.md` — If admin credentials are forgotten/compromised

---

## Revision History

| Version | Date       | Notes                                                                                                                                                |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for NetLink NL-3000 v2.x firmware; added DHCP scope exhaustion escalation criteria; clarified hard reset procedure to prevent POS disruption |
| 1.1     | 2024-11-20 | Added Resolution Path E for high system load; improved client log troubleshooting in Step 5                                                          |
| 1.0     | 2024-06-01 | Initial version; core diagnostic and resolution paths                                                                                                |

---

**Last Reviewed:** 2025-09-15  
**Next Review Due:** 2026-03-15  
**Owner:** L2 Wireless Infrastructure Team  
**Contact for Updates:** wireless-team@servewell-hospitality.local
