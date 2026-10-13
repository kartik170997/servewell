# Printer Offline or Not Detected

## Overview

This runbook addresses situations where receipt and kitchen printers (Epson TM-T88VI or Star MC Print v2) appear offline in the POS system or Windows, fail to print, or are not recognized by the device. Diagnosis and resolution steps differ between USB-connected and network-connected printers.

## Affected Systems

- **Printers:** Epson TM-T88VI (all variants), Star MC Print v2
- **POS Systems:** ServeWell POS v8.x and later
- **Operating Systems:** Windows 7 SP1, Windows 10 (all versions), Windows 11
- **Drivers:** Epson TM-T88VI Driver v3.2.0 and later; Star MC Print Driver v2.8.0 and later
- **Network:** TCP/IP network printers with static or DHCP IP assignment

## Symptoms

- Printer shows "Offline" status in ServeWell POS system
- Printer does not appear in Windows Devices and Printers
- "Printer not found" or "Communication error" messages in POS
- Print jobs queue but do not output
- USB printer not recognized by Windows Device Manager
- Network printer IP address unreachable or not detected
- Printer appears in Device Manager with yellow warning triangle (driver issue)
- Recent system update or network change coincides with failure

## Immediate Steps (First 2 Minutes)

1. **Physical Check**
   - Verify the printer is powered on (check LED indicator)
   - For USB printers: confirm cable is firmly connected to both printer and POS terminal
   - For network printers: confirm ethernet cable is firmly connected and switch/router is powered on

2. **Printer Self-Test**
   - Press and hold the **FEED button** on the printer for 3–5 seconds to initiate self-test
   - Verify paper loads and prints test pattern (confirms hardware is functional)
   - If self-test prints successfully, issue is driver or connectivity related

3. **Restart POS Application**
   - Close ServeWell POS completely
   - Wait 10 seconds
   - Reopen ServeWell POS and check if printer status updates to "Online"

---

## L1 Diagnosis Steps

### For USB Printers

**Step 1: Verify Device Recognition**

1. On the POS terminal, open **Settings** → **Devices** → **Printers & Scanners**
2. Locate the printer model (Epson TM-T88VI or Star MC Print v2)
3. **If printer is not listed:**
   - Disconnect USB cable from printer
   - Wait 5 seconds
   - Reconnect USB cable
   - Wait 10 seconds for Windows to detect device
   - Return to **Printers & Scanners** and refresh (F5)
4. **If printer appears with yellow warning icon:**
   - Note the warning; this indicates a driver problem (proceed to Step 3)
5. **If printer appears with green checkmark:**
   - Proceed to Step 2

**Step 2: Check Printer Status in Device Manager**

1. Press **Windows Key + R**, type `devmgmt.msc`, and press Enter
2. Expand **Printers** category
3. Locate your printer model
4. **If status shows error code:**
   - Note the exact error code (e.g., "Code 10," "Code 43")
   - Document for escalation
5. **If no error is shown:**
   - Proceed to Step 4 (Windows Spooler check)

**Step 3: Check Driver Version**

1. In **Printers & Scanners**, right-click the printer → **Properties**
2. Click the **Hardware** tab
3. Select the printer and click **Properties**
4. Click the **Driver** tab
5. Note the **Driver Version** displayed
   - **Epson TM-T88VI:** Should be v3.2.0 or later
   - **Star MC Print v2:** Should be v2.8.0 or later
6. **If version is older than listed above:**
   - Proceed to L1 Resolution Step 2 (Update Driver)
7. **If version is current:**
   - Proceed to Step 4

**Step 4: Verify Windows Print Spooler Service**

1. Press **Windows Key + R**, type `services.msc`, and press Enter
2. Scroll to locate **Print Spooler** service
3. Check the **Status** column
4. **If status shows "Stopped":**
   - Right-click **Print Spooler** → **Start**
   - Verify status changes to "Running"
5. **If status shows "Running":**
   - Restart the spooler: right-click → **Restart**

---

### For Network Printers

**Step 1: Verify IP Address and Network Connectivity**

1. On the printer itself, press and hold the **FEED button** and **POWER button** simultaneously for 5 seconds to print network configuration page
2. Locate the **IP Address** line on the printout
3. Note the IP address (format: `192.168.x.x` or `10.x.x.x`)
4. **If no IP address is displayed or shows `0.0.0.0`:**
   - Printer has not obtained an IP address (DHCP failure or static config issue)
   - Proceed to L1 Resolution Step 1
5. **If IP address is displayed:**
   - Proceed to Step 2

**Step 2: Test Network Connectivity from POS Terminal**

1. On the POS terminal, open **Command Prompt** as Administrator (Windows Key + R → `cmd` → Ctrl+Shift+Enter)
2. Type the command: `ping [IP_ADDRESS]` (replace [IP_ADDRESS] with the printer's IP from Step 1)
3. Press Enter
4. **If response shows "Reply from [IP_ADDRESS]":**
   - Printer is reachable on network; proceed to Step 3
5. **If response shows "Request timed out" or "Destination host unreachable":**
   - Network connectivity issue (firewall, VLAN, or network misconfiguration)
   - Proceed to L1 Resolution Step 1

**Step 3: Verify Printer Configuration in ServeWell POS**

1. Open ServeWell POS
2. Navigate to **Settings** → **Devices** → **Printers** (or equivalent menu path for your POS version)
3. Locate the network printer configuration
4. **Verify the following:**
   - Printer IP Address matches the address from Step 1 (exact match required)
   - Port number is `9100` (standard for thermal printers)
   - Printer is marked as **Enabled** or **Active**
5. **If IP address or port is incorrect:**
   - Update the configuration with correct values
   - Click **Save** or **Apply**
   - Proceed to Step 4
6. **If all settings appear correct:**
   - Proceed to Step 4

**Step 4: Check Printer Web Interface (Optional, Advanced)**

1. Open a web browser on the POS terminal
2. Navigate to `http://[IP_ADDRESS]` (use printer's IP address from Step 1)
3. **If web interface loads:**
   - Verify **Device Status** shows "Ready" or "Online"
   - Check **Network Settings** tab for IP configuration
4. **If web interface does not load:**
   - Network connectivity issue or printer web server is disabled

---

## L1 Resolution

### For USB Printers

**Resolution Step 1: Restart Windows Print Spooler Service**

1. Press **Windows Key + R**, type `services.msc`, and press Enter
2. Locate **Print Spooler** in the list
3. Right-click **Print Spooler** → **Restart**
4. Wait for status to show "Running"
5. Close Services window
6. Restart ServeWell POS application
7. Test printer by attempting a test print from POS

**Resolution Step 2: Update or Reinstall Driver**

1. Visit the manufacturer's support website:
   - **Epson:** https://epson.com (search "TM-T88VI")
   - **Star:** https://www.star-m.jp/products/s_print/tm-m30.html
2. Download the latest driver for your operating system
3. **To update driver in Windows:**
   - Press **Windows Key + R**, type `devmgmt.msc`, and press Enter
   - Expand **Printers**
   - Right-click your printer → **Update driver**
   - Select **Browse my computer for drivers**
   - Navigate to the downloaded driver file
   - Click **Next** and follow prompts
   - Restart the POS terminal when prompted
4. **If update fails, perform clean reinstall:**
   - In Device Manager, right-click the printer → **Uninstall device**
   - Check "Delete the driver software for this device"
   - Click **Uninstall**
   - Disconnect USB cable
   - Restart POS terminal
   - Reconnect USB cable (Windows will auto-detect)
   - Manually install driver from downloaded file (repeat steps above)

**Resolution Step 3: Clear Print Queue**

1. Press **Windows Key + R**, type `services.msc`, and press Enter
2. Right-click **Print Spooler** → **Stop**
3. Wait 5 seconds
4. Open File Explorer and navigate to: `C:\Windows\System32\spool\PRINTERS`
5. Delete all files in this folder (it will appear empty if queue is clear)
6. Return to Services, right-click **Print Spooler** → **Start**
7. Close Services and File Explorer
8. Restart ServeWell POS
9. Attempt a test print

---

### For Network Printers

**Resolution Step 1: Verify and Correct Network Configuration**

1. **If printer has no IP address (showing `0.0.0.0`):**
   - Power off the printer (hold POWER button 3 seconds)
   - Wait 10 seconds
   - Power on the printer
   - Wait 30 seconds for DHCP assignment
   - Print network configuration page again (hold FEED + POWER 5 seconds) to verify new IP address
   - If still no IP address, proceed to "When to Escalate" (network infrastructure issue)

2. **If printer IP address has changed unexpectedly:**
   - Assign a **static IP address** to prevent future changes
   - Access printer web interface at `http://[CURRENT_IP]`
   - Navigate to **Network Settings** or **TCP/IP**
   - Change from **DHCP** to **Static IP**
   - Assign a stable IP address (e.g., `192.168.1.100`) in coordination with your network administrator
   - Save and reboot printer

**Resolution Step 2: Update Printer Firmware (If Available)**

1. Visit the printer manufacturer's support website
2. Check for firmware updates for your printer model and current version
3. Download the firmware file to a USB drive
4. Follow manufacturer instructions to install firmware via printer's web interface or USB
5. Reboot printer after update completes
6. Verify printer comes online in POS

**Resolution Step 3: Correct POS Printer Configuration**

1. Open ServeWell POS
2. Navigate to **Settings** → **Devices** → **Printers**
3. Locate the network printer entry
4. **Update the following fields to match the printer's network configuration page:**
   - **Printer IP Address:** Exact IP from network configuration printout
   - **Port:** `9100` (default for thermal printers)
   - **Printer Name:** Match the name on configuration page (optional but recommended)
   - **Status:** Ensure marked as **Enabled** or **Active**
5. Click **Save** or **Apply**
6. Exit settings and perform a test print
7. **If test print succeeds:** Issue resolved
8. **If test print fails:** Proceed to next step

**Resolution Step 4: Restart Network Device Communication**

1. In ServeWell POS, navigate to **Settings** → **Devices**
2. Select the network printer and click **Disconnect** (or equivalent)
3. Wait 10 seconds
4. Click **Connect** to reinitialize communication
5. Monitor the status field—it should change to "Online" within 15 seconds
6. Attempt a test print
7. **If still offline:** Escalate to L2 with network printer IP address and POS configuration details

---

## When to Escalate to L2

**Escalate to L2 Support when any of the following conditions are met:**

1. **USB Printer Issues:**
   - Device Manager shows yellow warning icon with error code (Code 10, 43, or others) after driver reinstall
   - USB device is not detected after multiple connect/disconnect cycles
   - Driver installation fails with error message
   - Printer appears in Device Manager but print jobs do not output after spooler restart and queue clearing

2. **Network Printer Issues:**
   - Printer cannot obtain IP address after power cycle and 2-minute wait
   - `ping` command shows "Destination host unreachable" and network infrastructure has been verified as functional
   - Printer IP address is reachable but does not respond on port 9100
   - POS configuration is correct but printer still shows "Offline" after disconnect/reconnect cycle
   - Firmware update fails or printer becomes unresponsive after update attempt
   - Multiple printers on same network are affected (indicates network or POS configuration issue)

3. **General Escalation Criteria:**
   - Issue persists after completing all L1 Resolution steps
   - Hardware malfunction suspected (printer does not power on, LED indicators non-functional, self-test fails to print)
   - Error messages contain unfamiliar error codes or reference system/driver files
   - Printer was working previously; no recent changes to network, POS software, or drivers

**Information to Collect Before Escalating:**

- **Printer Model and Serial Number:** (printed on device label or network configuration page)
- **Printer Firmware Version:** (from network configuration page or web interface)
- **Current Driver Version:** (from Device Manager or Printers & Scanners properties)
- **Exact Error Messages:** (screenshots if possible; include error codes)
- **Device IP Address:** (for network printers; output of `ping` command)
- **POS System Configuration:** (screenshot of printer settings from ServeWell POS)
- **ServeWell POS Version:** (found in **Help** → **About** or **Settings**)
- **Windows OS Version:** (Settings → System → About)
- **Timestamp of Last Successful Print:** (helps determine when issue began)
- **Recent Changes:** (network changes, OS updates, driver updates, POS updates in last 7 days)
- **Test Print Results:** (success/failure status from POS application)

---

## Related Runbooks

- `Printer-Paper-Jam-or-Hardware-Error.md`
- `POS-Network-Connectivity-Troubleshooting.md`
- `Windows-Print-Spooler-Service-Issues.md`
- `ServeWell-POS-Device-Configuration.md`
- `Epson-TM-T88VI-Maintenance-and-Cleaning.md`
- `Star-MC-Print-v2-Setup-Guide.md`

---

## Revision History

| Version | Date       | Notes                                                                                                                             |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for current system versions; added Step 2 in L1 Diagnosis (Device Manager check); clarified DHCP vs. static IP resolution |
| 1.1     | 2024-11-20 | Expanded network printer troubleshooting; added web interface access steps                                                        |
| 1.0     | 2024-06-01 | Initial version                                                                                                                   |
