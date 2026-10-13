# POS Receipt Printer Integration Issues

## Overview

This runbook addresses POS receipt printer connectivity and configuration problems in FoodTech POS v4.2.x and v5.1.x environments. When the POS system cannot communicate with receipt printers (EpsonTM-T88VI or StarMC Print v2), transactions cannot complete properly, impacting store operations and customer service.

## Affected Systems

- **POS Software:** FoodTech POS v4.2.x, v5.1.x
- **Printer Models:** EpsonTM-T88VI, StarMC Print v2
- **Network:** Ethernet-connected printers on store LAN
- **Operating System:** Windows 7 Embedded/Windows 10 IoT (POS terminals)

## Symptoms

- POS displays "Printer Offline" error at transaction completion
- Receipts print to incorrect location (kitchen vs. customer receipt printer)
- Receipts print with garbled characters, missing sections, or cut off mid-transaction
- POS hangs for 30+ seconds during checkout, then times out
- Printer power LED is on, but POS cannot detect device
- Partial receipts print (header only, no items/totals)
- Same receipt prints to multiple printers simultaneously

## Immediate Steps (First 2 Minutes)

1. **Power Cycle the Printer**
   - Press and hold the power button on the receipt printer for 10 seconds until it fully shuts down
   - Wait 30 seconds
   - Press power button again to restart
   - Observe that the power LED illuminates and paper feed mechanism initializes

2. **Verify Printer Is Physically Connected**
   - Check Ethernet cable is firmly seated in printer's network port
   - Check cable is connected to the store network switch (not directly to POS terminal if using shared network)
   - Ensure no visible cable damage or pinched wires

3. **Check Printer Paper Supply**
   - Open printer cover and confirm receipt paper is loaded and not jammed
   - If jammed, remove obstruction and close cover firmly until it clicks
   - Press feed button once; paper should advance smoothly

---

## L1 Diagnosis Steps

### Step 1: Verify Printer Power and Network Connectivity

1. Confirm printer power LED is **solid green** (not amber/blinking)
   - If amber or off, perform full power cycle (see Immediate Steps)
2. Check that printer's **network LED is lit** (usually green or blue on rear panel)
   - If not lit, network cable may be disconnected or faulty (see **printer-offline.md**)
3. From the POS terminal, open **Command Prompt** (Run → `cmd.exe`)
4. Type `ping [printer-ip-address]` and press Enter
   - Printer IP address is typically printed on a configuration page (hold printer's reset button 3 seconds, let it print)
   - Expected result: "Reply from [IP]: bytes=32 time<100ms TTL=64"
   - If "Request timed out," printer is unreachable on network; escalate to L2

### Step 2: Access FoodTech POS Printer Configuration Menu

1. On the POS terminal, log in with **Manager credentials**
2. Navigate to **Settings → Hardware Configuration** (path varies by version):
   - **v5.1.x:** Settings icon (gear) → Hardware → Receipt Printers
   - **v4.2.x:** Manager Menu → System Setup → Peripherals → Printers
3. Locate the **"Configured Printers"** list
4. Note the following details for each printer:
   - Printer **Name** (e.g., "Kitchen Receipt #1")
   - Printer **IP Address** (should match physical printer IP from Step 1)
   - Printer **Model** (should show "EpsonTM-T88VI" or "StarMC Print v2")
   - Printer **Status** (should display "Active" or "Connected")
   - Printer **Port Assignment** (which receipts print here: Kitchen/Customer/Manager)

### Step 3: Check Printer Connection Status Within POS

1. In the Hardware Configuration menu, select the affected printer from the list
2. Click **"Test Connection"** button
3. Observe the response:
   - **Success message:** "Printer [name] is online and responding"
     - If you see this but printer still shows offline at checkout, proceed to Step 4
   - **Timeout error:** "Unable to contact printer. Check network connection."
     - Verify ping succeeded in Step 1; if yes, printer driver may need reinstall (escalate to L2)
   - **Device not found error:** Printer IP address in POS does not match actual printer IP
     - Proceed to Step 5
   - **Connection refused (Port 9100):** Printer driver not running or printer requires configuration
     - Escalate to L2

### Step 4: Review Printer Role and Port Assignment

1. Still in Hardware Configuration, check the **"Receipt Type"** or **"Printer Role"** setting for each printer
2. Verify assignments match business logic:
   - One printer should be designated **Kitchen Printer** (receives food/drink orders)
   - One printer should be designated **Customer Receipt Printer** (final transaction receipts)
   - Optional: **Manager Report Printer** (end-of-day reports)
3. If a printer is assigned to the **wrong role**, select it and click **"Edit"** or **"Change Role"**
4. Select the correct role from the dropdown and click **"Save"**
5. Return to Point of Sale and attempt a test transaction

### Step 5: Verify Printer IP Address Configuration

1. On the POS terminal, print a printer configuration page:
   - Hold the **reset button** (small recessed button on rear of printer) for 3 seconds
   - Printer will print a page showing its current IP address, MAC address, and settings
2. Compare the printed IP address with the address shown in POS Hardware Configuration (Step 2)
3. If they **do not match:**
   - Note the **correct IP from the printed configuration page**
   - Return to POS Hardware Configuration
   - Select the affected printer and click **"Edit"**
   - Update the **IP Address** field to match the printed configuration
   - Click **"Save"**
4. Perform another **Test Connection** (Step 3)

### Step 6: Check Print Driver and Emulation Settings

1. In Hardware Configuration, select the printer and click **"Properties"** or **"Advanced Settings"**
2. Verify the **Emulation Mode** setting:
   - EpsonTM-T88VI should be set to **"ESC/POS"** (Epson Standard)
   - StarMC Print v2 should be set to **"Star Proprietary"** or **"Star Line Mode"**
   - If incorrect, change to the correct mode and click **"Save"**
3. Check **Baud Rate** (if shown):
   - Should be **9600 bps** for network printers (higher rates not needed)
4. Note any **communication errors** or **warnings** displayed in the Properties dialog
   - If seen, take a screenshot and escalate to L2

---

## L1 Resolution

### Resolution A: Printer Shows Offline After Power Cycle and Connectivity Check

**Applies to:** Steps 1–3 completed successfully; "Test Connection" succeeds but POS still shows offline at checkout

1. Navigate to **Settings → Hardware Configuration → [Affected Printer]**
2. Click **"Offline/Online Toggle"** button (or **"Reset Connection"**)
3. Wait 15 seconds for the POS to re-establish communication
4. Check the status field; it should now display **"Active"**
5. Return to the Point of Sale screen and process a **test transaction** (void it immediately if needed)
6. Confirm receipt prints correctly to the correct printer
7. If still offline, proceed to Resolution B

### Resolution B: Printer IP Address Mismatch or Incorrect Configuration

**Applies to:** Step 5 identifies IP mismatch or Step 4 shows incorrect printer role

1. Obtain the **correct printer IP** from the configuration page (Step 5)
2. In Hardware Configuration, select the affected printer
3. Click **"Edit"** and update:
   - **IP Address** field to the correct address
   - **Printer Role** to the correct assignment (Kitchen/Customer/Manager)
   - **Emulation Mode** to match printer model (Step 6)
4. Click **"Save"**
5. Perform **Test Connection** and wait for success message
6. Return to POS and process a test transaction
7. Verify receipt prints to the correct location with correct formatting

### Resolution C: Garbled or Partial Receipts

**Applies to:** Receipts print with corrupted characters, missing items, or incomplete content

1. Check **print quality** issues first:
   - Verify **paper is loaded correctly** and not jammed
   - Ensure **printhead is clean** (use lint-free cloth with 70% isopropyl alcohol if visibly dirty)
   - Confirm **paper type** is standard receipt stock (not curled, wet, or expired)
2. In Hardware Configuration, select the printer and open **Properties**
3. Under **Print Settings**, check:
   - **Print Density:** Should be set to **100%** for standard receipt stock
   - **Paper Width:** Should match printer specs (typically 80mm for TM-T88VI, 58mm or 80mm for StarMC)
   - If adjusted, click **"Save"** and test print again
4. If garbling persists, check **driver version:**
   - Right-click the printer in **Devices and Printers** (Windows Control Panel)
   - Select **"Printer Properties"** → **"Advanced"** tab
   - Note the driver name and version (e.g., "Epson TM-T88VI v4.02")
   - If driver is older than 6 months, escalate to L2 for driver update
5. Test a receipt; if still garbled, escalate to L2

### Resolution D: Multiple Printers Receiving the Same Receipt

**Applies to:** Single receipt prints to two or more printers simultaneously

1. In Hardware Configuration, review all configured printers
2. Check that **only one printer** is assigned to **"Customer Receipt"** role
3. Check that **only one printer** is assigned to **"Kitchen"** role (if applicable)
4. If multiple printers have the **same role**, select the duplicates one at a time:
   - Click **"Edit"**
   - Change role to **"Unused"** or delete the configuration if it is a duplicate entry
   - Click **"Save"**
5. Return to POS and process a test transaction
6. Verify receipt prints to **only one printer**
7. If duplication persists, escalate to L2 with details of all configured printers

---

## When to Escalate to L2

Escalate to L2 Technical Support if **any** of the following conditions apply after completing the L1 Diagnosis and Resolution steps:

### Escalation Criteria

- **Network ping fails** (Step 1): Printer IP is unreachable; possible network/switch issue
- **Test Connection returns "Connection Refused"** or **"Port 9100 timeout"** (Step 3): Printer driver or firmware problem
- **Printer IP cannot be determined** (Step 5): Printer may need manual IP assignment via Ethernet configuration interface
- **Emulation Mode or Print Settings cannot be changed** or revert after saving: Permission or driver issue
- **Garbled receipts persist** after print density adjustment (Resolution C, Step 4)
- **Receipt duplication persists** after correcting printer roles (Resolution D, Step 6)
- **POS application crashes** during printer testing
- **Multiple printers offline simultaneously:** Possible network switch/VLAN configuration issue
- **Error codes** such as "E01," "E02," or "E99" appear in Hardware Configuration

### Information to Collect Before Escalating

Prepare the following details in a ticket or email to L2:

1. **Store Location** and **Terminal ID** (e.g., "Downtown Store, Register #3")
2. **POS System Version** (confirm v4.2.x or v5.1.x from Settings → About)
3. **Printer Model(s)** and **Serial Numbers** (visible on rear label)
4. **Printer IP Address(es)** and **MAC Address(es)** (from configuration page)
5. **All Steps Completed:**
   - Which numbered steps in L1 Diagnosis were performed?
   - Which resolution step was attempted (A/B/C/D)?
   - What was the exact result or error message?
6. **Screenshots:** Capture Hardware Configuration menu, Test Connection results, and any error messages
7. **Network Information:**
   - Is printer on same subnet as POS terminal? (provide subnet mask if known)
   - Are there any network switches, VLANs, or firewalls between POS and printer?
8. **Print Sample:** If receipts are garbled, attach a photo of the garbled receipt
9. **Timeline:** When did the issue start? Any recent changes (software updates, network changes, printer moves)?

---

## Related Runbooks

- **printer-offline.md** — Hardware checks, cable diagnostics, and printer power troubleshooting
- **foodtech-pos-network-setup.md** — POS network configuration and IP assignment for printers
- **epson-tm-t88vi-manual.md** — Detailed printer specifications and firmware information
- **star-mc-print-v2-configuration.md** — StarMC Print v2 setup and driver installation
- **pos-transaction-timeout-errors.md** — General checkout timeout issues and solutions
- **windows-iot-print-driver-management.md** — Print driver installation and updates on POS terminals

---

## Revision History

| Version | Date       | Notes                                                                                            |
| ------- | ---------- | ------------------------------------------------------------------------------------------------ |
| 1.2     | 2025-09-15 | Updated for FoodTech POS v5.1.x; added emulation mode checks; clarified printer role assignments |
| 1.1     | 2024-12-10 | Added garbled receipt troubleshooting; expanded escalation criteria                              |
| 1.0     | 2024-06-01 | Initial version for v4.2.x systems                                                               |

---

**Document Owner:** ServeWell Hospitality IT Help Desk  
**Last Updated:** 2025-09-15  
**Review Schedule:** Quarterly or after major POS/printer firmware updates
