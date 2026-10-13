# POS PIN Pad Not Responding

## Overview

The PIN pad (Ingenico Move 5000 or Verifone Vx820) is unresponsive to customer card transactions, displaying a blank screen, refusing input, showing connection errors, or not being recognized by the FoodTech POS system. This runbook provides L1 agents with diagnostic and resolution steps to restore payment processing functionality.

## Affected Systems

- **Ingenico Move 5000** (firmware v4.2.x - v4.5.x)
- **Verifone Vx820** (firmware v8.1.x - v8.3.x)
- **FoodTech POS** (v7.0 and later)
- **Connection types**: USB (recommended) and RS-232 Serial
- **Operating environment**: Windows 7 Professional SP1 or later; Windows 10/11 Pro

## Symptoms

- PIN pad screen is completely blank or unresponsive to touch
- PIN pad does not accept card input or shows "Device Not Ready" message
- PIN pad displays "Connection Error," "Device Offline," or error code E001/E002/E003
- FoodTech POS displays "PIN Pad Unavailable" or "No Payment Device Detected"
- PIN pad is physically powered on but unresponsive to any buttons or prompts
- Payment transactions fail with message "Terminal not responding"
- PIN pad appears in Device Manager with yellow exclamation mark or question mark
- Intermittent connectivity (device works occasionally, then disconnects)

## Immediate Steps (First 2 Minutes)

**Store staff should attempt these steps before calling IT:**

1. **Power cycle the PIN pad**: Unplug the USB cable (or serial cable) from the PIN pad for 30 seconds, then reconnect. Do NOT restart the entire POS system yet.

2. **Check physical connections**: Verify that:
   - USB cable (or serial cable) is fully seated into both the PIN pad and the POS terminal
   - No cable damage, kinks, or loose connectors are visible
   - Cable is not unplugged from the back of the POS computer

3. **Restart FoodTech POS application only**: Close FoodTech POS (do not restart Windows), wait 15 seconds, and reopen the application. Observe whether PIN pad reconnects automatically.

---

## L1 Diagnosis Steps

### Step 1: Verify PIN Pad Power and Basic Function

1. Check that the PIN pad has a solid power light (LED indicator typically green or blue, depending on model)
   - **Ingenico Move 5000**: Look for steady green light on top-left corner
   - **Verifone Vx820**: Look for steady blue light on top panel
2. If there is no power light, check that the power adapter is plugged into a working outlet and that the barrel connector is secure at the PIN pad
3. If still no power, proceed to "When to Escalate to L2" (hardware failure suspected)

### Step 2: Check FoodTech POS Logs for Error Codes

1. On the POS terminal, open **FoodTech POS application**
2. Navigate to: **Settings** → **System Diagnostics** → **Device Status**
3. Look for the PIN Pad entry and note the exact status and any error code displayed
   - **E001**: Device not detected (USB/Serial not recognized)
   - **E002**: Device detected but not responding
   - **E003**: Driver missing or outdated
4. Document the error code verbatim for escalation if needed

### Step 3: Check Windows Device Manager

1. On the POS terminal, open **Device Manager**:
   - Right-click **Start** menu → **Device Manager**, OR
   - Press `Windows Key + X` → **Device Manager**
2. Expand **Ports (COM & LPT)** for serial connections OR **Universal Serial Bus controllers** for USB
3. Look for:
   - Ingenico or Verifone device entry (should be present with no warning symbols)
   - Any device with yellow exclamation mark (?) or red X (indicates driver issue)
   - Unknown Device entries (may indicate unrecognized PIN pad)
4. **Note the exact device name and port number** (e.g., "COM3" or "USB Composite Device")

### Step 4: Test Connection Type and Cable

1. **For USB connections:**
   - Unplug USB cable from PIN pad and POS terminal
   - Wait 10 seconds
   - Plug into a **different USB port** on the back of the POS terminal (try USB 2.0 if available; avoid USB hubs)
   - Return to Device Manager (F5 refresh) and verify device reappears
   - If device appears in new port, the original port may be faulty

2. **For Serial (RS-232) connections:**
   - Note the COM port from Device Manager (e.g., COM3)
   - Verify the cable connector is a standard 9-pin or 25-pin serial connector (visually inspect)
   - Try a different serial port on the POS terminal if available

### Step 5: Verify FoodTech POS PIN Pad Configuration

1. In **FoodTech POS**, navigate to: **Settings** → **Payment Devices** → **PIN Pad Configuration**
2. Verify the following settings match the actual device:
   - **Device Type**: Select correct model (Ingenico Move 5000 OR Verifone Vx820)
   - **Connection Type**: USB or Serial (match actual physical connection)
   - **COM Port** (Serial only): Confirm port number matches Device Manager
   - **Baud Rate** (Serial only): Should be 9600 for standard installations
3. Take a screenshot of this screen for documentation
4. Click **Test Connection** button and observe for 10 seconds
   - Success: "Connection Successful" message appears
   - Failure: Note exact error message displayed

---

## L1 Resolution

### Resolution Path 1: Driver Reinstall (Most Common Fix)

**Applies to**: Error codes E003, yellow exclamation mark in Device Manager, or "Device Not Recognized"

1. **Uninstall current driver**:
   - Open **Device Manager**
   - Locate the PIN pad device (or "Unknown Device" with yellow mark)
   - Right-click → **Uninstall device**
   - Check box: **Delete the driver software for this device**
   - Click **Uninstall** and wait for completion

2. **Remove hardware**:
   - Unplug USB cable (or serial cable) from both PIN pad and POS terminal
   - Wait 30 seconds

3. **Obtain correct driver**:
   - **Ingenico Move 5000**: Download from `\\fileserver\IT\Drivers\Ingenico\Move5000_v4.5_Driver.exe`
   - **Verifone Vx820**: Download from `\\fileserver\IT\Drivers\Verifone\Vx820_v8.3_Driver.exe`
   - Alternatively, request drivers from **IT Service Desk** (ticket preferred)

4. **Install driver** (execute as Administrator):
   - Double-click the driver .exe file
   - Follow on-screen prompts (default settings acceptable)
   - When prompted, **do not** plug in the PIN pad yet
   - Restart the POS terminal when prompted by installer
   - Allow 2-3 minutes for Windows to fully boot

5. **Reconnect hardware**:
   - After Windows fully boots, plug in USB cable (or serial cable)
   - Windows should detect device and apply driver automatically
   - Return to **Device Manager** and verify device now appears without warning symbols

6. **Test in FoodTech POS**:
   - Open **FoodTech POS** → **Settings** → **Payment Devices** → **PIN Pad Configuration**
   - Click **Test Connection**
   - If successful, proceed to verification steps below

### Resolution Path 2: FoodTech POS Configuration Reset

**Applies to**: No hardware errors in Device Manager, but FoodTech reports "Device Unavailable"

1. **Backup current configuration** (optional but recommended):
   - In **FoodTech POS**, navigate to **Settings** → **Backup/Export**
   - Select **Export System Configuration**
   - Save file to Desktop with timestamp (e.g., `POS_Config_2025-02-14.bak`)

2. **Reset PIN pad configuration**:
   - In **FoodTech POS**, go to **Settings** → **Payment Devices** → **PIN Pad Configuration**
   - Click **Reset to Defaults** button
   - When prompted, confirm: "This will disconnect the current PIN pad and reset connection settings"
   - Click **Yes**

3. **Reconfigure PIN pad**:
   - **Device Type**: Select the appropriate model from dropdown (Ingenico Move 5000 or Verifone Vx820)
   - **Connection Type**: Select USB or Serial based on physical cable
   - **COM Port** (Serial only): Select the port from Device Manager (e.g., COM3)
   - **Baud Rate** (Serial only): Leave at 9600
   - Click **Save**

4. **Test connection**:
   - Click **Test Connection** button
   - Wait 10 seconds for result
   - Successful result: "PIN Pad Connected Successfully"

### Resolution Path 3: USB Port or Cable Issue

**Applies to**: Device works intermittently or only after power cycling

1. **Test with alternate USB port**:
   - Unplug PIN pad USB cable
   - Plug into a different USB port on the rear of the POS terminal
   - Return to FoodTech POS → **Settings** → **Payment Devices** → **PIN Pad Configuration**
   - Click **Test Connection**
   - If this port works, the original port may be faulty; note and document for L2

2. **Inspect USB cable**:
   - Visually examine entire length of USB cable for:
     - Bent or damaged connectors
     - Cuts, pinches, or exposed wires
     - Kinks or stress points
   - If damage visible, request replacement cable from IT Service Desk

3. **Test with replacement USB cable**:
   - If IT provides a spare cable, disconnect current cable and connect spare
   - Plug into same USB port as before
   - Test connection in FoodTech POS
   - If replacement cable works, original cable is defective; escalate for replacement

### Resolution Path 4: Serial (RS-232) Connection Troubleshooting

**Applies to**: Error E001 or "Device Not Detected" on serial connections

1. **Verify serial connection settings in FoodTech POS**:
   - In **FoodTech POS** → **Settings** → **Payment Devices** → **PIN Pad Configuration**
   - Confirm **COM Port** matches the port shown in Device Manager (e.g., COM3, COM4)
   - Confirm **Baud Rate** is set to 9600
   - Click **Save**

2. **Test the serial port**:
   - In **Device Manager**, right-click the COM port → **Properties**
   - Click **Port Settings** tab
   - Verify **Bits per second**: 9600
   - Verify **Data bits**: 8
   - Verify **Parity**: None
   - Verify **Stop bits**: 1
   - Verify **Flow control**: None
   - Click **OK**

3. **Reconnect PIN pad**:
   - Unplug serial cable from PIN pad
   - Wait 10 seconds
   - Plug serial cable back in firmly (should click into place)
   - In FoodTech POS, click **Test Connection**

---

## Verification Steps (All Paths)

After completing any resolution path, perform these verification steps:

1. **Test in FoodTech POS**:
   - Navigate to **Settings** → **Payment Devices** → **PIN Pad Configuration**
   - Click **Test Connection**
   - Verify PIN pad responds with "Connection Successful" message
   - Leave window open for 15 seconds to confirm no disconnection

2. **Perform a test transaction** (if possible at store):
   - On the POS terminal, initiate a test payment transaction
   - Insert or swipe a test card (contact IT if no test card available)
   - Verify PIN pad displays "Enter PIN" or payment prompt
   - Complete transaction (can void after successful processing)

3. **Document resolution**:
   - Note which resolution path was used
   - Document any error codes encountered
   - Record timestamp of successful reconnection

---

## When to Escalate to L2

**Escalate immediately if any of the following conditions exist:**

### Hardware Failure Indicators

- PIN pad has no power light and power adapter is confirmed working
- Physical damage visible on PIN pad (cracked screen, broken connector, water damage)
- PIN pad device appears in Device Manager but cannot be uninstalled
- Error code E999 or "Hardware Failure" displayed in FoodTech POS

### Persistent Connection Failures

- PIN pad fails to connect after completing both "Driver Reinstall" and "FoodTech POS Configuration Reset" paths
- PIN pad connects in one USB port but fails in all other USB ports (indicates mainboard failure on POS terminal)
- Serial port fails to detect PIN pad even after verifying all settings and reseating cable

### Cable/Port Issues

- Visible damage to USB cable that cannot be replaced by store staff
- Multiple USB ports on POS terminal are non-functional
- Serial connector is damaged or bent beyond repair

### Unknown Errors

- Any error code not listed in this runbook (E004, E100, etc.)
- FoodTech POS crashes when attempting to test PIN pad connection
- Device Manager shows "Unknown Device" that cannot be identified after driver installation

### Information to Collect Before Escalating

Gather the following information and include in your escalation ticket:

1. **Store location and terminal ID**
2. **PIN pad model and serial number** (found on back of device)
3. **PIN pad firmware version**: In FoodTech POS → **Settings** → **System Diagnostics** → **Device Status** → **PIN Pad Info**
4. **Exact error code** from FoodTech POS or Device Manager
5. **Connection type**: USB or Serial, and port number (e.g., COM3)
6. **Steps already completed**: List all L1 resolution paths attempted and results
7. **Screenshots**: Device Manager status, FoodTech POS error message, PIN Pad Configuration screen
8. **Timeline**: When issue started, whether it was working previously, any recent changes to POS system

**Example escalation ticket summary**:

> "Store #4521 | Verifone Vx820 (S/N 5VB7T2E) | Error E002 | USB Port 2 | Attempted: Driver Reinstall + FoodTech Reset. Device appears in Device Manager but connection test fails. Ready for L2 hardware diagnostics."

---

## Related Runbooks

- `POS-System-Startup-Procedure.md` — Full POS terminal boot and initialization steps
- `FoodTech-POS-Application-Crash.md` — Troubleshooting application errors and recovery
- `Network-Connectivity-Diagnostics.md` — Checking POS internet and network connections
- `Windows-Device-Manager-Issues.md` — General hardware device troubleshooting
- `PIN-Pad-Payment-Processing-Errors.md` — Transaction-level payment failures
- `Hardware-Replacement-Procedures.md` — Ordering and installing replacement PIN pads
- `Ingenico-Move5000-Factory-Reset.md` — PIN pad-level factory reset procedures
- `Verifone-Vx820-Firmware-Update.md` — PIN pad firmware upgrade steps

---

## Revision History

| Version | Date       | Notes                                                                                                                  |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1.3     | 2025-02-14 | Added serial connection troubleshooting; expanded resolution paths; updated driver links for current firmware versions |
| 1.2     | 2025-09-15 | Updated for current system versions; added Device Manager screenshots guidance                                         |
| 1.0     | 2024-06-01 | Initial version                                                                                                        |

---

**Document Owner**: ServeWell IT Service Desk | **Last Updated**: 2025-02-14 | **Review Cycle**: Quarterly
