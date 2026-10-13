# Slow Network / Bandwidth Issues

## Overview

Staff report internet connectivity is functional but significantly degraded, with web pages loading slowly, timeouts on online ordering systems, and delayed transaction processing. This runbook addresses diagnosis and resolution of bandwidth throttling and network performance degradation on ServeWell hospitality locations using NetLink NL-3000 v2.x infrastructure.

## Affected Systems

- **NetLink NL-3000 v2.0** through **v2.1+** network appliance
- POS systems (all models) communicating via NL-3000
- Online ordering platforms and payment gateways
- Kitchen display systems (KDS)
- Guest Wi-Fi services (where applicable)
- Staff management and reporting systems

## Symptoms

- Web pages load slowly or timeout (>10 seconds for standard pages)
- Online order submissions fail or display "Connection Timeout" errors
- POS transactions process normally but payment authorization delays occur
- Streaming services or downloads extremely slow (if in use)
- Video calling or remote support tools disconnect unexpectedly
- Speed test results show <25% of expected ISP bandwidth
- Multiple users report simultaneous slowness (not isolated to single device)
- Guest Wi-Fi performs significantly slower than wired connections
- Email sync failures or attachment download timeouts
- Intermittent disconnections with automatic reconnection

## Immediate Steps (First 2 Minutes)

**Store staff can perform these checks before contacting IT:**

1. **Restart the primary router:** Unplug the NetLink NL-3000 device for 30 seconds, then reconnect. Wait 3-5 minutes for full bootup (all indicator lights should stabilize).

2. **Check for obvious obstructions:** Verify the NL-3000 device has clear airflow, is not blocked by equipment, and all cable connections are firmly seated in ports.

3. **Test from different locations:** Have staff attempt to load a simple website (e.g., google.com) from both wired and wireless connections to determine if the issue affects all devices or is location-specific.

4. **Note the exact time slowness began:** This helps IT correlate with usage patterns, backup windows, or system events.

## L1 Diagnosis Steps

### Step 1: Verify Connectivity Status

1. Open a web browser on any device connected to the network.
2. Navigate to the NL-3000 management dashboard: **https://192.168.1.1** (default gateway).
3. Log in using L1 credentials (username: **support_l1**, password stored in SecurePass vault).
4. Verify the status page shows:
   - **WAN Link Status:** GREEN (Connected)
   - **Internet Connection:** Active
   - **All interface lights** on the physical device showing GREEN or AMBER (not RED)
5. If RED lights or "Disconnected" status appears, skip to **Step 5: Physical Connection Check**.

### Step 2: Run Automated Speed Test

1. From the NL-3000 dashboard, navigate to **Diagnostics > Speed Test**.
2. Click **Start Speed Test** (test takes 2-3 minutes; do not interrupt).
3. Upon completion, note the following metrics:
   - **Download Speed** (Mbps)
   - **Upload Speed** (Mbps)
   - **Latency/Ping** (ms)
4. Compare results to the service contract ISP speeds:
   - **Expected:** Check ticket header or contact L2 if unknown
   - **Acceptable threshold:** ≥80% of contracted speed
   - **Poor threshold:** <50% of contracted speed
5. **Document all three metrics.** This is critical for escalation.

### Step 3: Check DHCP Pool Status (Critical for v2.1)

1. From the NL-3000 dashboard, go to **Network > DHCP Server**.
2. Locate the **DHCP Pool Utilization** indicator (displays as percentage).
3. Note the current values:
   - **Current Active Leases:** **_ / _** (e.g., 247/250)
   - **Pool Utilization %:** \_\_\_%
4. **If utilization is >85%, this is likely the cause** (especially on v2.1 where throttling occurs at 90%+).
5. Scroll down to **Active DHCP Leases** and note:
   - How many devices are connected
   - Whether any devices have inactive leases (stale entries consuming pool space)

### Step 4: Review QoS Policy Status

1. Navigate to **Network > Quality of Service (QoS)**.
2. Confirm the current active policy: **Look for "POS_Priority_v2.1"** or similar (should be displayed at top).
3. Verify the policy status shows **ENABLED** (green checkmark).
4. Under **Traffic Classes**, confirm:
   - **POS Systems:** Priority = **High** (this is correct)
   - **General Internet:** Priority = **Standard** (this is correct)
   - **Guest Wi-Fi:** Priority = **Low** (expected)
5. Check **Bandwidth Allocation:**
   - POS should show 40-50% reserved
   - General Internet should show 30-40% available
   - If allocation shows POS at >60%, note this for escalation
6. **Do not adjust QoS settings at L1 level.**

### Step 5: Physical Connection Check

1. **Inspect the NL-3000 device back panel:**
   - Verify WAN port (typically labeled **WAN** or **Internet**) has a cable firmly connected
   - Verify at least one LAN port has connection (green light indicator)
   - Check that power cable is fully seated
2. **If disconnected:** Reconnect firmly and wait 2 minutes for reconnection.
3. **Return to Step 1** to verify reconnection.

### Step 6: Check for Known Scheduled Maintenance

1. Access the ServeWell IT portal: **https://support.servewell.internal**
2. Navigate to **Maintenance Schedule** in the left sidebar.
3. Check if there is scheduled maintenance within the past 24 hours or upcoming.
4. **If maintenance occurred in past 8 hours,** this may explain temporary degradation. Escalate only if slowness persists >2 hours post-maintenance.

## L1 Resolution

### Resolution Path A: DHCP Pool Exhaustion (Most Common on v2.1)

**Applicable if:** DHCP pool utilization is >85% (Step 3, above).

1. Navigate to **Network > DHCP Server** (as in Step 3).
2. Click **Active DHCP Leases** tab.
3. **Identify stale leases:**
   - Sort by "Last Activity" (oldest first).
   - Look for devices showing no activity for >4 hours.
   - These are typically printers, guest devices, or disconnected endpoints.
4. Select checkbox next to the oldest stale lease and click **Release Lease**.
5. Repeat for next 5-10 oldest inactive leases until pool utilization drops below 80%.
   - **Note:** Do not release leases for POS terminals, KDS units, or devices with recent activity.
6. **Verify the fix:**
   - Ask staff to test web browsing and online ordering.
   - Rerun speed test in 2 minutes (allow time for devices to reconnect).
   - Document new speed test results.
7. **If utilization climbs back above 85% within 30 minutes,** the issue is device proliferation or misconfigured device behavior. Escalate to L2.

### Resolution Path B: QoS Misconfiguration

**Applicable if:** QoS shows incorrect allocation or is DISABLED (Step 4 status is red).

1. Navigate to **Network > Quality of Service (QoS)**.
2. **If policy is DISABLED (red):**
   - Click **Enable** button.
   - Confirm policy name is **"POS_Priority_v2.1"**.
   - Click **Apply**.
   - Wait 30 seconds for policy to activate (light should turn green).
3. **If policy is enabled but allocation is abnormal:**
   - Click **Edit Policy**.
   - Verify the following allocations match exactly:
     - **POS Systems:** 45% reserved bandwidth
     - **General Internet:** 35% available bandwidth
     - **Guest Wi-Fi:** 15% available bandwidth
     - **Management Traffic:** 5% reserved
   - If percentages differ, **do not adjust.** Escalate to L2 immediately with screenshot.
4. **Rerun speed test** and confirm results improve.
5. Ask staff to test online ordering specifically (most QoS-sensitive function).

### Resolution Path C: ISP-Level Throttling

**Applicable if:** Speed test shows consistently <50% of contracted speed and physical connections are verified.

1. Document the following before escalation:
   - Current speed test results (from Step 2)
   - Time slowness began
   - Whether slowness is constant or intermittent
   - DHCP pool utilization (from Step 3)
   - Active QoS policy name and status (from Step 4)
2. **Contact the ISP directly** using the number on the service invoice:
   - Provide the speed test results and contracted speed.
   - Ask if there are any line issues, congestion, or throttling events.
   - Request they run diagnostics on the WAN line.
3. **Escalate to L2 immediately** with ISP response and all diagnostic data (see **When to Escalate to L2** section below).

### Resolution Path D: Network Congestion / Rogue Application

**Applicable if:** Speed test shows acceptable speeds, but users still report slowness (suggests local application consuming bandwidth).

1. Navigate to **Network > Traffic Monitor**.
2. Click **Top Talkers** tab.
3. **Identify unusual traffic:**
   - Look for non-POS applications consuming >10 Mbps continuously.
   - Note the source IP address and application/protocol.
4. **Common offenders:**
   - Windows Update (OS updates on shared devices)
   - Backup software running during business hours
   - Streaming services on staff devices
5. **Action items:**
   - Identify the source device (correlate IP to MAC address if needed).
   - Contact the location manager or department head to identify the device owner.
   - Request the offending application be closed or scheduled for off-hours.
   - **Do not force-terminate without authorization.**
6. Rerun speed test after application is closed.
7. If high-bandwidth traffic is unidentifiable, escalate to L2.

## When to Escalate to L2

Escalate a ticket to L2 Support immediately if **any** of the following conditions are met:

### Escalation Criteria

1. **DHCP Pool exhaustion persists after releasing stale leases** (multiple cycles of purging within 1 hour)
2. **Speed test shows <50% of contracted ISP speed AND physical connections verified**
3. **QoS policy shows RED status (disabled) and cannot be re-enabled**
4. **QoS bandwidth allocation does not match standard percentages** (see Resolution Path B)
5. **WAN port shows RED or repeatedly disconnects** after physical verification
6. **Multiple stale DHCP leases from unknown devices** suggesting potential security issue
7. **Speed test results fluctuate wildly** (>50% variance in consecutive tests)
8. **Unknown high-bandwidth traffic identified** in Traffic Monitor
9. **Network completely unavailable** (cannot reach NL-3000 dashboard or no internet at all)
10. **Issue persists >1 hour after all L1 resolution steps attempted**

### Information to Collect Before Escalating

Gather the following data and include in the escalation ticket:

- [ ] **Speed test results:** Download, Upload, Ping (Mbps and ms)
- [ ] **Contracted ISP speed** (from service contract or ticket header)
- [ ] **DHCP pool utilization %** and active lease count
- [ ] **Current QoS policy name** and status (enabled/disabled)
- [ ] **Screenshot of NL-3000 dashboard status page** (showing all interface lights)
- [ ] **Exact time slowness began**
- [ ] **List of resolution steps attempted** (A, B, C, or D above)
- [ ] **Any error messages** observed on user devices (type exactly as displayed)
- [ ] **Number of affected users** (all staff, specific department, etc.)
- [ ] **Network device count** from DHCP active leases
- [ ] **ISP response** (if contacted in Resolution Path C)
- [ ] **System version:** NL-3000 v2.0 or v2.1+

### Escalation Template

Use the following template when opening an L2 ticket:

```
ESCALATION: Slow Network / Bandwidth Issues - [Location Name]

ISSUE SUMMARY:
[1-2 sentence description of reported slowness]

SPEED TEST RESULTS:
- Download: ___ Mbps (Expected: ___ Mbps)
- Upload: ___ Mbps (Expected: ___ Mbps)
- Ping: ___ ms

L1 RESOLUTION ATTEMPTS:
- [ ] Path A: DHCP pool purging (unsuccessful)
- [ ] Path B: QoS re-enabled (unsuccessful)
- [ ] Path C: ISP contacted (response: ___)
- [ ] Path D: Rogue application identified (___) (unsuccessful)

CURRENT SYSTEM STATUS:
- DHCP Pool Utilization: ___%
- QoS Policy: ___ [Status: Enabled/Disabled]
- NL-3000 Version: v2.___
- All WAN/LAN lights: [Green/Amber/Red]

BUSINESS IMPACT:
[Describe impact on POS, ordering, etc.]

ATTACHMENTS:
- Dashboard status page screenshot
- Speed test results screenshot
- Any relevant error messages
```

## Related Runbooks

- [NetLink_NL3000_Dashboard_Access.md](NetLink_NL3000_Dashboard_Access.md)
- [DHCP_Pool_Management.md](DHCP_Pool_Management.md)
- [QoS_Configuration_Baseline.md](QoS_Configuration_Baseline.md)
- [ISP_Troubleshooting_Escalation.md](ISP_Troubleshooting_Escalation.md)
- [Network_Device_Inventory_Audit.md](Network_Device_Inventory_Audit.md)
- [POS_System_Network_Diagnostics.md](POS_System_Network_Diagnostics.md)
- [Traffic_Analysis_and_Monitoring.md](Traffic_Analysis_and_Monitoring.md)

## Revision History

| Version | Date       | Notes                                                                                                                                     |
| ------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated DHCP pool exhaustion procedures for v2.1; added Traffic Monitor section for Resolution Path D; clarified QoS baseline allocations |
| 1.1     | 2024-12-01 | Added escalation template; expanded Step 3 with pool utilization thresholds; reorganized resolution paths for clarity                     |
| 1.0     | 2024-06-01 | Initial version; covered basic speed test and QoS diagnostics                                                                             |

---

**Knowledge Base Category:** Network Infrastructure  
**Last Reviewed:** 2025-09-15  
**Next Review Date:** 2025-12-15  
**Owner:** ServeWell IT Support — L1/L2 Team
