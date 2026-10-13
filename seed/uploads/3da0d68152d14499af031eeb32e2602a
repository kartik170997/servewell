# Printer Incorrect Format / Blank / Garbled Output

## Overview

Guest receipts are printing blank, displaying garbled/corrupted characters, or in incorrect format, typically affecting POS transactions and kitchen orders. This issue commonly occurs after driver updates, thermal head degradation, or character encoding mismatches between the POS system and printer firmware.

## Affected Systems

- **Hardware**: Epson TM-T88VI (thermal receipt printer)
- **Software**: StarMC Print v2.x (v2.4.0 and later)
- **POS Integration**: ServeWell POS Suite v4.x+
- **Operating System**: Windows 7 SP1+, Windows Server 2012 R2+

## Symptoms

- Receipts print completely blank (no text or images)
- Characters display as random symbols, boxes, or unreadable garbled text
- Text appears in wrong position (off-center, cut off, or misaligned)
- Special characters (£, €, ®, ™) render as question marks or spaces
- Receipt format missing logos, barcodes, or header/footer information
- Intermittent printing issues (some orders print correctly, others fail)
- Kitchen display system (KDS) orders printing incorrectly
- Printer status appears normal (online, ready) but output is corrupted

## Immediate Steps (First 2 Minutes)

1. **Power Cycle the Printer**
   - Power off the Epson TM-T88VI using the rear power switch
   - Wait 30 seconds
   - Power on and wait for the startup sequence to complete (LED should be solid green)

2. **Verify Paper Supply**
   - Ensure thermal receipt paper is loaded correctly (shiny side down, toward the print head)
   - Check that paper is not jammed or stuck in the feed mechanism
   - Confirm paper type matches specifications (80mm width, thermal-sensitive)

3. **Request a Manual Test Print**
   - Ask store staff to use the physical **FEED button** on the printer (located on top panel) to advance paper
   - Press and hold the **FEED button** for 2 seconds—this triggers the factory test pattern
   - Observe output: if test pattern prints clearly, the hardware is functional

## L1 Diagnosis Steps

### Step 1: Verify Printer Hardware Status

1. Locate the **Status LED indicator** on the front of the Epson TM-T88VI
   - **Solid Green** = Online and ready
   - **Blinking Green** = Processing data
   - **Red** = Error condition (paper out, cover open, thermal head error)
2. If LED is **Red**, check:
   - Printer cover is fully closed
   - Paper is loaded and not jammed
   - Thermal head is not visibly damaged (should be smooth, shiny metal surface)
3. If LED remains Red after power cycle, escalate to L2 with photo of LED status

### Step 2: Check Driver Installation

1. On the POS terminal, open **Settings** → **Devices and Printers**
2. Locate **Epson TM-T88VI** in the device list
3. Right-click → **Printer properties** → **Advanced** tab
4. Verify driver version:
   - Expected: **Epson TM-T88VI v6.xx** or higher (not v5.xx or older)
   - Note exact version number for escalation if needed
5. If driver version is older than v6.0:
   - **Do not update now**—contact L2 first (known compatibility issues with StarMC Print v2.4.0+)

### Step 3: Review Recent System Changes

1. Ask the store manager:
   - When did the problem start? (Today? After maintenance window? After restart?)
   - Were any Windows updates applied in the last 7 days?
   - Was the printer driver updated recently?
   - Have there been any POS system updates?
2. Document findings in the ticket—this directs L2 toward root cause

### Step 4: Test StarMC Print v2 Configuration

1. On the POS terminal, open **StarMC Print v2** (typically in Program Files\StarMC\)
2. Navigate to **Settings** → **Printer Configuration**
3. Verify the following settings:
   - **Printer Model**: Epson TM-T88VI
   - **Port**: COM3 or USB (verify the correct port is selected)
   - **Character Encoding**: **JIS** (not UTF-8 or ASCII)
   - **Receipt Width**: **80mm**
   - **Print Speed**: **Normal** (not High Speed)
4. If encoding is set to anything other than **JIS**, note this—it is likely the root cause

### Step 5: Generate a Test Receipt

1. In the POS interface, navigate to **Reports** → **Test Print**
2. Select **Receipt Format: Standard Guest Receipt**
3. Select **Printer: Epson TM-T88VI**
4. Click **Print Test Receipt**
5. Observe the output:
   - **Clear text, correct format** = Printer is functioning (may be application-level issue)
   - **Blank** = Hardware or driver failure
   - **Garbled/unreadable** = Encoding mismatch (proceed to Resolution Step 2)
   - **Format misaligned** = Print width setting incorrect (proceed to Resolution Step 3)

### Step 6: Inspect Thermal Print Head (If Safe to Do)

1. **Power off the printer and unplug from wall outlet**
2. Open the printer cover (lift the metal bar on top)
3. Visually inspect the **thermal print head** (silver metallic element running horizontally):
   - Look for dark spots, burns, or visible cracks
   - Check for dried ink residue or paper debris
4. If head appears damaged or heavily soiled, escalate to L2 with photo
5. If head appears clean, proceed to Resolution Step 1

## L1 Resolution

### Resolution Step 1: Clean the Thermal Print Head (If Visibly Dirty)

1. **Printer must be powered off and unplugged**
2. Prepare a lint-free cloth slightly dampened (not wet) with **99% isopropyl alcohol**
3. Gently wipe the thermal print head from left to right, using light pressure
   - Do **not** use paper towels, tissues, or abrasive materials
   - Do **not** apply excessive pressure or solvents other than isopropyl alcohol
4. Allow 2 minutes for alcohol to evaporate
5. Plug in the printer and power on
6. Run test print (Diagnosis Step 5)
7. If issue persists, escalate to L2

### Resolution Step 2: Correct Character Encoding in StarMC Print v2

**This is the most common fix for garbled characters.**

1. On the POS terminal, open **StarMC Print v2**
2. Navigate to **Settings** → **Printer Configuration**
3. Under **Character Encoding**, verify the setting:
   - If set to **UTF-8** or **ASCII**: change to **JIS** (Japanese Industrial Standard)
   - If already set to **JIS**: change to **UTF-8**, wait 5 seconds, change back to **JIS** (reset the setting)
4. Click **Save** and **Apply**
5. Close StarMC Print v2 completely (verify in Task Manager that no StarMC process is running)
6. Wait 10 seconds
7. Reopen StarMC Print v2
8. Run test receipt print (Diagnosis Step 5)
9. If garbled characters persist, escalate to L2 with screenshot of encoding setting and sample photo of garbled output

### Resolution Step 3: Adjust Print Width and Format Settings

1. Open **StarMC Print v2** → **Settings** → **Printer Configuration**
2. Verify **Receipt Width**: should be set to **80mm** (not 58mm or 110mm)
3. Navigate to **Receipt Format** tab
4. Confirm **Left Margin**: 0mm, **Top Margin**: 5mm (standard defaults)
5. If margins or width are non-standard, reset to defaults and click **Restore Factory Settings**
6. Click **Save** and **Apply**
7. Close StarMC Print v2 and reopen
8. Run test receipt print (Diagnosis Step 5)
9. If format remains incorrect, escalate to L2

### Resolution Step 4: Update Printer Driver (Only if Approved by L2)

**Contact L2 before proceeding—driver compatibility is a known issue.**

1. If L2 approves, download the latest Epson TM-T88VI driver from Epson support portal:
   - Search: "Epson TM-T88VI driver Windows 7/10/Server 2012 R2"
   - Current safe version: **v6.12a** (verify with L2)
2. Uninstall existing driver:
   - **Settings** → **Devices and Printers** → Right-click **Epson TM-T88VI** → **Remove device**
   - Restart system
3. Install new driver from downloaded executable
4. Restart system again
5. Run test print (Diagnosis Step 5)
6. If issue persists after driver update, escalate to L2 with driver version and any error messages from installation

### Resolution Step 5: Power Cycle and Factory Reset (Last Attempt Before Escalation)

1. Power off printer and POS terminal simultaneously
2. Wait 60 seconds
3. Power on printer first, wait for startup sequence to complete (solid green LED)
4. Power on POS terminal
5. Wait for Windows to fully load and all services to start (approximately 3 minutes)
6. Open StarMC Print v2
7. Run test print (Diagnosis Step 5)
8. If issue persists, escalate to L2

## When to Escalate to L2

Escalate immediately with the following information if any of these conditions apply:

### Escalation Criteria

- Thermal print head shows visible damage, burn marks, or cracks
- Printer LED is **Red** and persists after power cycle and paper/cover checks
- Test print remains **completely blank** after all Resolution steps
- Garbled characters persist after correcting character encoding to JIS
- Driver version is **older than v5.0** or **newer than v6.12a** (outside safe range)
- Issue started immediately after Windows security update or POS system patch
- Multiple printers on the same network are affected
- Intermittent failures suggest hardware degradation (issue worsens over time)

### Information to Collect Before Escalating

1. **Printer Details**:
   - Printer model and serial number (located on back panel)
   - Printer LED status (color and blink pattern)
   - Driver version (from Devices and Printers)

2. **Software Versions**:
   - StarMC Print v2 exact version number
   - POS Suite version
   - Windows OS version and last update date

3. **Timeline**:
   - Exact date/time issue started
   - Any recent system changes (updates, restarts, configuration changes)
   - Whether issue is intermittent or persistent

4. **Test Results**:
   - Outcome of test print (Diagnosis Step 5)
   - Character encoding setting in StarMC Print v2
   - Screenshot or photo of garbled/blank output
   - Photo of thermal print head condition (if visually inspected)

5. **Store Context**:
   - Number of affected printers
   - Whether other printers on the same network are working
   - Approximate number of failed receipts in the last 24 hours

### How to Escalate

1. In the ServeWell IT Help Desk ticketing system, create a new **L2 Technical Escalation** ticket
2. Set **Priority** to **High** (if affecting active transactions) or **Medium** (if intermittent)
3. Attach collected diagnostic information and photos
4. Reference this runbook section in notes: "Escalated per Printer Incorrect Format / Blank / Garbled Output runbook"
5. Notify L2 team via Slack channel #printer-support

## Related Runbooks

- [Printer_Offline_Not_Responding.md](./Printer_Offline_Not_Responding.md)
- [StarMC_Print_v2_Installation_Configuration.md](./StarMC_Print_v2_Installation_Configuration.md)
- [POS_Terminal_Hardware_Diagnostics.md](./POS_Terminal_Hardware_Diagnostics.md)
- [Thermal_Printer_Maintenance_Schedule.md](./Thermal_Printer_Maintenance_Schedule.md)
- [Windows_Driver_Update_Procedure.md](./Windows_Driver_Update_Procedure.md)

## Revision History

| Version | Date       | Notes                                                                                                         |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for StarMC Print v2.4.0+; clarified JIS encoding requirement; added thermal head inspection procedure |
| 1.1     | 2024-12-10 | Added driver compatibility warning; expanded escalation criteria                                              |
| 1.0     | 2024-06-01 | Initial version                                                                                               |

---

**Document Owner**: ServeWell Hospitality IT Support  
**Last Reviewed**: 2025-09-15  
**Next Review**: 2025-12-15
