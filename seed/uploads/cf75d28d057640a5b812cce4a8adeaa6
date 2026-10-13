# Specific Devices Not Connecting to Network

## Overview

A single device or small group of devices cannot establish network connectivity while other devices at the same location connect normally. This runbook helps L1 agents quickly isolate and resolve connectivity issues affecting specific endpoints without impacting store operations.

## Affected Systems

- **NetLink NL-3000** (v3.2.1 and later)
- **Cisco SG350-28** (firmware v2.4.8.26 and later)
- **Cisco SG350-52** (firmware v2.4.8.26 and later)
- Connected endpoints: POS terminals, kitchen displays, wireless tablets, printers, IP phones

## Symptoms

- Single device unable to obtain IP address (displays "No Connection" or similar)
- Device shows "Unidentified Network" or "Limited Connectivity"
- Device was previously connected but now drops off network
- Device connects via WiFi but not wired Ethernet (or vice versa)
- Other devices at same location connect without issue
- "Cannot reach DHCP server" error messages
- Device repeatedly disconnects/reconnects
- Device assigned static IP but cannot communicate with network

## Immediate Steps (First 2 Minutes)

Store staff or on-site manager should attempt these checks before contacting IT:

1. **Restart the device** – Power cycle by disconnecting power for 30 seconds, then reconnect
2. **Check physical connections** – Verify Ethernet cable is fully seated in both device and wall jack (for wired devices)
3. **Check WiFi availability** – Confirm the SSID is visible and in range (for wireless devices)
4. **Test another device** – Attempt connecting a different device to the same cable/WiFi to determine if issue is device-specific or infrastructure-wide

## L1 Diagnosis Steps

### Step 1: Gather Device Information

1. Obtain the **device MAC address**:
   - **POS Terminal**: Navigate to System Settings > Network > Device Information; note MAC address
   - **Kitchen Display**: Check label on back of unit (format: `XX:XX:XX:XX:XX:XX`)
   - **IP Phone**: Press **Settings** button > **System** > **Information**; locate MAC address
   - **Wireless Tablet**: Go to Settings > About Device > look for "MAC Address" or "WiFi MAC"

2. Confirm the **device type, model, and location** (store number, area)

3. Ask the user: _"When was this device last working?"_ and _"Has anything changed since then (cables, location, updates)?"_

### Step 2: Determine Connectivity Type

1. Confirm if device is attempting **wired (Ethernet)** or **wireless (WiFi)** connection
2. For wired devices: Verify Ethernet cable connects to correct switch port
3. For wireless devices: Confirm correct SSID name and password

### Step 3: Check DHCP Lease Status

**For wired devices via NetLink NL-3000:**

1. Log into NetLink NL-3000 web interface (IP: `10.0.0.1`, credentials per ticket system)
2. Navigate to **Administration > DHCP Server > Active Leases**
3. Search for the device's MAC address in the active leases table
4. **If lease is present**: Note the assigned IP address and lease expiration time
5. **If lease is absent**: Device has not contacted DHCP server; proceed to Step 4

**For wireless devices via Cisco SG350:**

1. Log into Cisco SG350 switch web interface (IP: `10.0.0.2`)
2. Navigate to **Switching > VLAN Management > VLAN List**
3. Identify the VLAN assigned to wireless traffic (typically VLAN 10 or 20)
4. Check **Administration > DHCP Server > Active Leases** for that VLAN
5. Search for the device's MAC address

### Step 4: Check MAC Address Filtering

**On NetLink NL-3000:**

1. Log into NetLink interface > **Security > MAC Filtering**
2. Verify the **Filter Mode** is set to:
   - **Disabled** (preferred for most environments), OR
   - **Whitelist Mode** (if enabled, the device MAC must appear in the approved list)
3. If in Whitelist Mode, check if the device's MAC is present in the approved list
4. **If MAC is missing and filter is enabled**: This is the likely cause

**On Cisco SG350:**

1. Log into Cisco SG350 web interface
2. Navigate to **Security > Port Security**
3. Select the port where the device connects
4. Confirm **Port Security Status** is **Disabled** or the device MAC is in the **Allowed Address** list
5. Note the **Maximum Addresses** setting (default is 1; if exceeded, new devices are blocked)

### Step 5: Check for IP Address Conflicts

1. **If device was assigned a static IP**: Obtain the assigned IP address from:
   - Device network settings, OR
   - Service ticket notes, OR
   - Store manager/on-site IT documentation
2. From a working device at the store, attempt to **ping the static IP**:
   - Open command prompt or terminal
   - Type: `ping [static IP address]` (e.g., `ping 10.0.100.50`)
   - **If ping succeeds but device still cannot connect**: IP conflict likely exists; another device is using this IP
   - **If ping times out**: IP is available but device is not online
3. Check NetLink DHCP leases table for any duplicate IPs assigned to different MACs

### Step 6: Verify Port Status on Switch

**For wired devices:**

1. Log into Cisco SG350 web interface
2. Navigate to **Port Status > Port List**
3. Locate the physical port where device connects (numbered 1-28 or 1-52)
4. Verify port shows **Status: Up** and **Link State: Up** (green indicator)
5. **If status shows Down/Disconnected**:
   - Ask user to physically reseat the Ethernet cable
   - Wait 10 seconds and refresh the page
   - If still Down, note port number for escalation

## L1 Resolution

### Resolution A: Clear DHCP Lease and Reconnect (Common Fix)

1. **Power cycle the device**: Disconnect power for 30 seconds, reconnect
2. Confirm device attempts to connect to network
3. Wait up to 2 minutes for DHCP lease to be assigned
4. Verify device obtains IP address in NetLink DHCP Active Leases table
5. Test connectivity (e.g., open web browser, ping gateway `10.0.0.1`)
6. **Document**: Note the assigned IP address in the ticket

### Resolution B: Remove MAC Address from Whitelist Block (If Applicable)

1. Confirm MAC Filtering is enabled on NetLink (see Step 4 above)
2. Log into NetLink > **Security > MAC Filtering**
3. Check if device's MAC appears in any **Block List** or is missing from **Allow List**
4. **If blocking is intentional**: Contact store manager to confirm removal is permitted
5. **To remove block**: Select the MAC address and click **Delete** or **Remove**
6. To add to whitelist: Click **Add** and enter the device MAC address
7. Wait 30 seconds and reboot the device
8. Verify device now obtains DHCP lease

### Resolution C: Release Static IP Conflict

1. Identify the conflicting static IP address (from Step 5)
2. **Option 1 – Reconfigure device to use DHCP**:
   - Access device network settings
   - Change from Static IP to **DHCP/Dynamic** mode
   - Reboot device
   - Verify device obtains new IP from DHCP server
3. **Option 2 – Reassign static IP to unused address**:
   - Use NetLink DHCP leases table to identify an available IP in the correct subnet
   - Manually reconfigure device with new static IP (not in any active lease)
   - Reboot and verify connectivity

### Resolution D: Reset Port on Cisco SG350

1. Log into Cisco SG350 web interface
2. Navigate to **Port Management > Port Configuration**
3. Select the physical port where device connects
4. Click **Reset Port** or toggle **Port Enable: Off** then **On**
5. Wait 30 seconds for port to come back up
6. Reboot the connected device
7. Verify device obtains DHCP lease

### Resolution E: Clear Port Security Violation (If Applicable)

1. Log into Cisco SG350
2. Navigate to **Security > Port Security > Violation Mode**
3. If port shows **Violation Status: True**:
   - Click **Clear Violation** for that port
   - Wait 10 seconds
4. Reboot the affected device
5. Verify connectivity

## When to Escalate to L2

Escalate to L2 Support immediately if:

### Escalation Criteria

- Device remains unable to connect **after completing all Steps 1–6 and attempting Resolutions A–E**
- Multiple devices in the same store cannot connect (indicates infrastructure issue, not device-specific)
- Switch port shows **Status: Down** even after reseating cables and resetting port (possible hardware failure)
- DHCP server shows **Error** or **Service Inactive** status in NetLink/Cisco admin interface
- Device obtains IP address but **cannot communicate with any network resource** (ping, DNS, gateway all fail)
- Port Security or MAC Filtering configuration has been modified recently and changes coincide with connectivity loss
- Error messages indicate **firmware mismatch** or **incompatible version** on device or switch

### Information to Collect Before Escalating

Provide L2 with the following in the ticket:

- [ ] **Device MAC address** and **currently assigned IP address** (if any)
- [ ] **Device type, model, and serial number**
- [ ] **Store location and specific area** (POS lane, kitchen, etc.)
- [ ] **Wired or wireless connectivity attempt**
- [ ] **Last known working date/time**
- [ ] **All diagnostic steps completed** and results:
  - DHCP lease status (present/absent)
  - MAC filter status and whether MAC is in allow/block list
  - Cisco SG350 port status (Up/Down, and which port number)
  - Any error messages displayed on device (exact text)
- [ ] **Screenshots** of:
  - NetLink DHCP Active Leases table
  - Cisco SG350 Port Status showing the relevant port
  - Device network settings showing MAC address and current IP
- [ ] **Changes made so far** and results

---

## Related Runbooks

- `netlink-nl3000-configuration.md`
- `cisco-sg350-port-management.md`
- `network-troubleshooting-general.md`
- `dhcp-server-issues.md`
- `wireless-connectivity-issues.md`
- `pos-terminal-setup.md`

---

## Revision History

| Version | Date       | Notes                                                                                                                       |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for NetLink v3.2.1 and Cisco SG350 firmware v2.4.8.26; clarified MAC filtering steps and added port reset procedure |
| 1.1     | 2024-12-10 | Added wireless device diagnostics and clarified escalation criteria                                                         |
| 1.0     | 2024-06-01 | Initial version                                                                                                             |
