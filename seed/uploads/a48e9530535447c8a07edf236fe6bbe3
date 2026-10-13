# Network Router Completely Offline

## Overview

This runbook addresses complete internet connectivity loss when the primary network router (NetLink NL-3000 v2.x or Cisco SG350) is unresponsive and all store systems cannot reach cloud-based services. Follow this guide to systematically diagnose whether the issue is hardware failure, ISP outage, or configuration error.

## Affected Systems

- **NetLink NL-3000 v2.x** (primary router)
- **Cisco SG350** (backup/secondary router)
- Point-of-Sale (POS) terminals
- Kitchen Display Systems (KDS)
- Cloud-based reporting services
- Payment processing gateways
- Staff scheduling and inventory platforms

## Symptoms

- No internet connectivity across all wired and wireless devices
- Router does not respond to ping requests (e.g., `ping 192.168.1.1`)
- All LED indicators on router are off or showing red/amber status
- POS systems display "No connection to cloud services" or timeout errors
- Mobile devices cannot connect to facility Wi-Fi
- Impossible to access router admin interface via web browser or SSH
- Store manager receives alerts about cloud service unavailability

## Immediate Steps (First 2 Minutes)

**Store staff or shift manager should attempt these checks before contacting IT:**

1. **Verify physical connections:** Check that all ethernet cables are firmly connected to the router's WAN (Internet) port and to the modem. Reseat any loose cables.

2. **Check upstream modem:** Confirm the modem (if separate from the router) has power and displays normal status lights. Ask store manager to power-cycle the modem if unresponsive.

3. **Confirm other stores are online:** Ask if neighboring locations or other branches are experiencing similar issues. This quickly identifies potential ISP-wide outages.

4. **Note the time and alert shift manager:** Document the outage start time and inform management of revenue impact.

---

## L1 Diagnosis Steps

### Step 1: Verify Physical Hardware Status

1. Locate the router in the network closet or back office.
2. Confirm power cable is connected and the router has electrical power (listen for fans, check that power indicator light is present).
3. **For NetLink NL-3000 v2.x:** Check the LED panel on the front:
   - **Green (Power):** Device is powered and functional.
   - **Red (Power):** Device is in error state; note this status.
   - **Amber (Internet):** Attempting connection or ISP issue detected.
   - **Red (Internet):** No ISP signal; ISP outage or WAN cable disconnected.
4. **For Cisco SG350:** Check LED ring around power button:
   - **Solid Green:** System operational.
   - **Blinking Green:** System booting or processing.
   - **Amber or Red:** Hardware fault or critical error.
5. **Document exact LED status** before proceeding to next step.

### Step 2: Check Physical Connectivity

1. Inspect the **WAN (Internet) port** on the router:
   - Ensure ethernet cable is fully inserted (you should hear a click).
   - If cable appears damaged or frayed, note it for replacement.
   - **For NetLink NL-3000 v2.x:** WAN port is labeled **"Internet In"** on the back panel.
   - **For Cisco SG350:** WAN uplink typically uses port 1 or the dedicated uplink port (verify local network diagram).

2. Inspect the **modem connection** (if a separate modem exists):
   - Verify cable from modem to router WAN port is secure.
   - Check modem power and status lights.
   - If modem shows no lights, power-cycle it: unplug for 30 seconds, plug back in, wait 2 minutes for full boot.

3. Verify at least one **LAN (local) port** connection to a test device (e.g., office computer):
   - Connect a laptop directly to one of the router's LAN ports with an ethernet cable.
   - Open a terminal/command prompt.
   - Run: `ping 192.168.1.1` (or confirm correct router IP from network diagram).
   - If ping succeeds, router is operational; proceed to Step 3.
   - If ping fails, note this and proceed to Step 3 (router may be in failed state).

### Step 3: Attempt Remote Access to Router Interface

1. Open a web browser on a device connected to the local network (LAN).
2. Navigate to the router's admin interface:
   - **NetLink NL-3000 v2.x:** `https://192.168.1.1` (username: `admin`, password: check credential vault)
   - **Cisco SG350:** `http://192.168.1.254` (default username: `Cisco`, password: per your network documentation)
3. **If interface loads:**
   - Log in and proceed to Step 4.
   - **If login fails:** Try default credentials (document the failure and escalate to L2 with error message).

4. **If interface does not load:**
   - Try alternative access method (SSH from command line):
     ```bash
     ssh admin@192.168.1.1
     ```
   - Note any error message (e.g., "Connection refused," "Connection timed out," "Host unreachable").
   - **If SSH also fails:** Router is unresponsive to network commands; escalate with status and LED information (see **When to Escalate to L2**).

### Step 4: Check WAN/Internet Connection Status

**If you successfully accessed the router interface:**

1. **For NetLink NL-3000 v2.x:**
   - Navigate to **Status → Internet Connection** or **Dashboard** tab.
   - Look for "WAN Status" field:
     - **Connected:** If displayed, the router sees the ISP connection. Test internet access from a workstation. If no internet access, check local DHCP/DNS settings (proceed to Step 5).
     - **Disconnected / No Signal:** Indicates ISP outage or WAN cable issue. Verify cable connection (Step 2) and contact ISP.
     - **Authenticating / Negotiating:** Router is attempting connection. Wait 3–5 minutes and refresh. If status persists, note the state and escalate.
   - Check **Internet LED** status on physical device (should be solid green if connected).

2. **For Cisco SG350:**
   - Navigate to **System → System Information** or **Status** page.
   - Look for "Link Status" on the uplink port (Port 1 or designated uplink):
     - **Link Up:** Physical connection established. Check IP configuration in next step.
     - **Link Down / No Link:** Physical connection failed; verify cable (Step 2) and escalate if cable is confirmed good.
   - Verify **IP Configuration** under **Network → Interfaces**:
     - Confirm WAN interface (e.g., `vlan99`) has a valid public IP address (not `0.0.0.0` or blank).
     - If IP is blank or `0.0.0.0` and DHCP is enabled, ISP is not assigning an address; contact ISP.

### Step 5: Verify ISP Connection and DNS

1. From the router interface, run a **Ping Test** to an external address:
   - **NetLink NL-3000 v2.x:** Go to **Tools → Diagnostics → Ping**.
     - Enter `8.8.8.8` (Google DNS).
     - Click **Ping** and observe results.
   - **Cisco SG350:** Use SSH and run:
     ```bash
     ping 8.8.8.8
     ```

2. **If ping to 8.8.8.8 succeeds:**
   - Internet connection is working from the router.
   - Issue is likely DNS, DHCP, or local network configuration.
   - Proceed to **L1 Resolution - DNS/DHCP Issue** (see below).

3. **If ping to 8.8.8.8 fails or times out:**
   - ISP connection is not functional.
   - Escalate to **When to Escalate to L2** with diagnostic results and contact ISP support in parallel.

---

## L1 Resolution

### Resolution A: Reboot Router (Most Common Fix)

**Perform this step if router is responsive but internet is unavailable:**

1. **Graceful reboot (preferred):**
   - Access router admin interface (see Step 3).
   - **For NetLink NL-3000 v2.x:** Navigate to **System → Reboot** and click **Reboot System**.
   - **For Cisco SG350:** Navigate to **System → Configuration → Reboot** and confirm.
   - Wait for device to power-cycle (listen for fans to restart; LED indicators will go dark then relight).
   - **Wait 5 minutes** for full boot before testing connectivity.

2. **If graceful reboot is unavailable (interface unresponsive):**
   - Perform **hard reboot:** Unplug power cable from router.
   - Wait **30 seconds** (capacitors discharge).
   - Plug power cable back in.
   - Wait **5 minutes** for full boot (observe LED indicators returning to normal green status).

3. **After reboot, test connectivity:**
   - From a local workstation, attempt to browse an external website (e.g., `http://example.com`).
   - Log into POS or cloud service to confirm connectivity is restored.
   - Check all LED indicators on the router for normal status (green lights for power and internet).

4. **If connectivity is restored:** Reboot resolved the issue. Document time of outage and reboot. Monitor for recurrence.

5. **If connectivity is not restored after reboot:** Proceed to Resolution B.

### Resolution B: Reset WAN/Internet Configuration

**Perform if reboot did not restore connectivity and router is responding:**

1. **Check DHCP and WAN settings:**
   - **For NetLink NL-3000 v2.x:**
     - Navigate to **Network → Internet Connection** or **WAN Settings**.
     - Verify **"Obtain IP Automatically (DHCP)"** is **enabled**.
     - Click **Renew DHCP Lease** if available.
     - Wait 1–2 minutes and refresh the page.
     - Confirm that WAN interface now has a valid IP address (not `0.0.0.0`).

   - **For Cisco SG350:**
     - Navigate to **Network → Interfaces**.
     - Select the WAN VLAN or uplink interface.
     - Verify IP address configuration is set to **DHCP** (not static unless documented otherwise).
     - If DHCP is enabled and no IP is assigned, disable then re-enable DHCP:
       - Click **Edit**, uncheck **DHCP Enable**.
       - Click **Apply**.
       - Edit again, check **DHCP Enable**.
       - Click **Apply** and wait 2 minutes.

2. **Verify DNS settings:**
   - **For NetLink NL-3000 v2.x:** Go to **Network → DNS Settings**.
     - Confirm **"Automatic DNS"** is **enabled**, or manually set primary DNS to `8.8.8.8` and secondary to `8.8.4.4` (Google Public DNS).
     - Click **Apply**.

   - **For Cisco SG350:** Go to **System → DNS**.
     - Verify at least one DNS server is configured (typically provided by ISP via DHCP).
     - If blank, manually add `8.8.8.8` as primary.

3. **Test connectivity after DNS/DHCP reset:**
   - Wait 2 minutes for settings to take effect.
   - From a local workstation, ping router gateway: `ping 192.168.1.1`.
   - Then ping external address: `ping 8.8.8.8`.
   - Attempt web browsing and cloud service access.

4. **If connectivity is restored:** Document the configuration change. Monitor for recurrence. Alert L2 team if DHCP/DNS resets become frequent.

5. **If connectivity is still not restored:** Escalate to L2 (see **When to Escalate to L2** below).

### Resolution C: Power Cycle Modem and Router (Sequence)

**If router is powered and responsive but no ISP connection:**

1. **Power off in sequence:**
   - Unplug the **modem** (if separate) and wait 30 seconds.
   - Unplug the **router** and wait 30 seconds.

2. **Power on in sequence:**
   - Plug in the **modem** and wait **2 minutes** for it to fully boot (observe status lights stabilizing).
   - Plug in the **router** and wait **3–5 minutes** for it to fully boot (observe LED indicators turning green).

3. **Test connectivity:**
   - From a workstation, verify WAN connection: `ping 8.8.8.8`.
   - Check router status interface for "Connected" or "Link Up" status.
   - Attempt to access cloud services from POS or office system.

4. **If connectivity is restored:** Document outage and power-cycle action. This typically indicates a transient ISP or modem issue.

5. **If connectivity is not restored:** Note the exact LED status on the router and proceed to escalation.

---

## When to Escalate to L2

**Escalate immediately to L2 Support if any of the following conditions are met:**

### Escalation Criteria

1. **Router is completely unresponsive:**
   - Cannot ping router IP address (e.g., `192.168.1.1`).
   - Cannot access web interface or SSH.
   - No LED indicators are lit on the device (except after hard reboot; wait 5 minutes).
   - **Action:** Escalate with LED status and confirmation that power cable is connected.

2. **WAN connection shows "No Signal" or "Disconnected" after cable verification:**
   - Physical WAN cable is confirmed connected and undamaged.
   - Router interface shows "No ISP Signal" or "WAN Disconnected."
   - Modem (if separate) is powered and operational.
   - **Action:** Escalate with ISP account number and last-known connection status. L2 will contact ISP.

3. **Ping to external address (8.8.8.8) fails consistently after all L1 steps:**
   - Router is responsive and WAN status shows "Connected."
   - DNS and DHCP are verified as configured correctly.
   - Multiple reboot and reset attempts have not restored connectivity.
   - **Action:** Escalate with ping test results and diagnostics.

4. **P1 Priority Outage during meal service periods (11:00 AM – 1:30 PM, 5:00 PM – 8:00 PM):**
   - Regardless of root cause, escalate immediately to L2 and notify the on-call manager.
   - Internet outage during peak service prevents POS transactions and payment processing.
   - **Action:** Page L2 senior technician and provide brief status summary (see below).

5. **Hardware failure is suspected:**
   - Router displays continuous error codes or error LED status that persist after reboot.
   - **For NetLink NL-3000 v2.x:** Red Power LED or blinking error indicators.
   - **For Cisco SG350:** Amber or Red LED status persisting after 5-minute boot period.
   - Unusual noises (clicking, grinding) or visible physical damage.
   - **Action:** Escalate with photographs of LED status and description of any physical damage.

### Information to Collect Before Escalating

Gather the following information to expedite L2 resolution:

- **Store Location and Store ID**
- **Outage Start Time** (as accurately as possible)
- **Current Date/Time** (for L2 to cross-reference logs)
- **Router Model and Version:**
  - **NetLink NL-3000 v2.x:** Check label on back of device; verify version number.
  - **Cisco SG350:** Access System Information page; note firmware version.
- **Exact LED Status:**
  - Power LED color (Green / Amber / Red / Off)
  - Internet/WAN LED color (Green / Amber / Red / Off)
  - Any blinking patterns
- **Results of ping tests:**
  - Can you ping `192.168.1.1`? (Yes / No / Timeout)
  - Can you ping `8.8.8.8`? (Yes / No / Timeout)
- **Router Admin Interface Status:**
  - Can you access web interface? (Yes / No / Error message)
  - If accessible, what is the WAN connection status shown?
- **Modem Status (if applicable):**
  - Is modem powered on? (Yes / No)
  - What color are modem status lights?
  - Model number of modem.
- **ISP Service Details (if available):**
  - ISP name and account number (for L2 to contact ISP if needed)
  - Any recent maintenance notifications from
