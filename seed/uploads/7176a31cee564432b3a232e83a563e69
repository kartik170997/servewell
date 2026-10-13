# POS Cash Drawer Not Opening

## Overview

The cash drawer fails to open when a sale is completed, a manual open command is issued, or opens unexpectedly during normal operations. This runbook covers diagnosis and resolution for FoodTech POS v4.2.x, v5.1.x, and OrbitPOS v2.x systems.

## Affected Systems

| System       | Versions                     | Notes                             |
| ------------ | ---------------------------- | --------------------------------- |
| FoodTech POS | v4.2.0–v4.2.8, v5.1.0–v5.1.4 | All hardware configurations       |
| OrbitPOS     | v2.0–v2.3.x                  | v2.0 has known drawer-on-void bug |

## Symptoms

- Cash drawer does not open after completing a sale transaction
- Manual drawer open button (in POS interface) produces no response
- Drawer remains stuck in closed position despite multiple open attempts
- Drawer opens randomly during non-drawer operations (e.g., inventory, void transactions)
- Audible buzzing or clicking from drawer unit without drawer opening
- Error message displayed: `ERR_DRAWER_TIMEOUT` or `DRAWER_COMM_FAIL`

## Immediate Steps (First 2 Minutes)

**Any store staff member can perform these checks:**

1. **Power cycle the drawer unit**: Locate the power cable at the rear of the cash drawer. Disconnect for 10 seconds, then reconnect. Wait 30 seconds for the unit to reinitialize.

2. **Check physical obstructions**: Open the drawer manually using the **manual override key** (located in the lock cylinder on the front-left of most drawers). Inspect for cash, receipts, or debris blocking the drawer mechanism. Remove any obstructions.

3. **Verify the drawer is fully closed**: Push the drawer firmly into the closed position until you hear a click. Press the manual open button on the POS screen once and wait 5 seconds.

If the drawer opens after these steps, no further troubleshooting is required. If the drawer remains stuck or unresponsive, proceed to L1 Diagnosis.

---

## L1 Diagnosis Steps

**Perform these steps in order. Document the results of each step.**

### Step 1: Verify POS System Status

1. Check the POS main screen for any warning banners or error indicators at the top of the display.
2. Note the exact POS version: Navigate to **Settings > System Information** and record the version number (e.g., FoodTech v5.1.2).
3. Confirm the POS system is fully booted and responsive (test by opening a menu or transaction).
4. **Document result**: System version, any error messages displayed.

### Step 2: Inspect Hardware Connection

1. Locate the cash drawer cable connection point on the back of the POS terminal.
2. **For FoodTech POS**: Drawer cable typically connects to a serial (COM) or USB port labeled "DRAWER" or "PORT 2."
3. **For OrbitPOS**: Drawer cable connects to the dedicated drawer port (typically RJ-12 jack on rear panel).
4. Gently wiggle the cable connection while observing the drawer for any response. Do not force the connector.
5. If the cable is loose, fully disconnect and reconnect it firmly. Wait 5 seconds and test drawer operation.
6. **Document result**: Cable connection status (loose/secure), any response observed.

### Step 3: Test Manual Open Command

1. From the POS main screen, navigate to **Settings > Hardware > Cash Drawer** (FoodTech) or **Admin > Peripherals > Drawer** (OrbitPOS).
2. Click the **Test Drawer** or **Manual Open** button.
3. Observe and listen to the drawer for 10 seconds:
   - Does the drawer solenoid buzz/click?
   - Does the drawer move or attempt to open?
   - Is there any response at all?
4. **Document result**: Solenoid response (none/buzzing/clicking), drawer movement, any error codes displayed on screen.

### Step 4: Check Drawer Configuration (FoodTech)

1. Navigate to **Settings > Hardware > Cash Drawer > Configuration**.
2. Verify the following settings match your hardware:
   - **Drawer Port**: Should match the physical connection (COM1, COM2, USB1, etc.). If you are unsure, try COM1 first.
   - **Drawer Type**: Verify it matches your physical drawer model (typically "Standard" or "Star" for FoodTech systems).
   - **Open Pulse Duration**: Should be 100–150 milliseconds. Document the current value.
3. If any setting appears incorrect, note it for L1 Resolution.
4. **Document result**: All configuration settings and values.

### Step 5: Check OrbitPOS Configuration (OrbitPOS Systems Only)

1. Open the OrbitPOS configuration file: Press **Ctrl + Alt + F12** to access the **Admin Console**.
2. Navigate to **System Configuration > Peripherals > Drawer**.
3. Locate the parameter **DRAWER_VOID**.
   - **If DRAWER_VOID=1**: The drawer will open on void transactions (known bug in v2.0). Note this for escalation.
   - **Document the current value**.
4. Also check **DRAWER_ENABLED** parameter—should be set to "1" (enabled).
5. **Document result**: DRAWER_VOID value, DRAWER_ENABLED value.

### Step 6: Review Recent Error Logs

1. **FoodTech POS**: Navigate to **Settings > System > Logs > Hardware Events**. Look for entries in the past 15 minutes containing "DRAWER", "TIMEOUT", or "COMM_FAIL".
2. **OrbitPOS**: Access **Admin Console > Logs > System**. Filter for entries containing "DRAWER".
3. **Document result**: Any error messages found, timestamps, and full error text.

---

## L1 Resolution

**Perform these steps in order for the most common causes. Test drawer operation after each step.**

### Resolution Step 1: Reseat the Drawer Cable

1. Power off the POS terminal completely (use the **Settings > Power Off** menu, or hold the power button for 5 seconds).
2. Locate the drawer cable at the rear of the POS unit.
3. Fully disconnect the cable from the POS port by gently pulling the connector straight out.
4. Wait 10 seconds.
5. Reconnect the cable firmly until you hear or feel a click. Do not force.
6. Power the POS terminal back on.
7. Wait 60 seconds for the system to fully boot.
8. Test the drawer by pressing the **Manual Open** button in Settings > Hardware > Cash Drawer.
9. **If resolved**: Document the successful resolution and close the ticket.
10. **If not resolved**: Proceed to Resolution Step 2.

### Resolution Step 2: Update Drawer Port Configuration (FoodTech Only)

1. Navigate to **Settings > Hardware > Cash Drawer > Configuration**.
2. If the **Drawer Port** is currently set to "COM2" or "USB1", change it to **"COM1"** and click **Save**.
3. The system will prompt you to restart—click **Yes**.
4. After restart, test the drawer.
5. **If unsuccessful**, return to the same menu and try **"USB1"** (if available) or the next sequential option.
6. Test after each change.
7. **Document result**: Which port setting resolved the issue, or note that changing the port did not help.
8. **If not resolved**: Proceed to Resolution Step 3.

### Resolution Step 3: Adjust Drawer Pulse Duration (FoodTech Only)

1. Navigate to **Settings > Hardware > Cash Drawer > Configuration**.
2. Locate **Open Pulse Duration** (measured in milliseconds).
3. If the current value is **100 ms**, increase it to **125 ms** and save.
4. Test the drawer.
5. If unsuccessful, increase to **150 ms** and test again.
6. **Do not exceed 150 ms** as this may damage the solenoid.
7. **Document result**: Which pulse duration resolved the issue, if any.
8. **If not resolved**: Proceed to Resolution Step 4.

### Resolution Step 4: Disable and Re-enable Drawer (Both Systems)

1. **FoodTech**: Navigate to **Settings > Hardware > Cash Drawer** and toggle **Drawer Enabled** to **OFF**. Click **Save**.
2. **OrbitPOS**: Access **Admin Console > System Configuration > Peripherals > Drawer** and set **DRAWER_ENABLED=0**.
3. Restart the POS system (**Settings > Power Off** or through Admin Console).
4. After boot, re-enable the drawer using the same menus (set to **ON** or **=1**).
5. Restart the POS system again.
6. Test the drawer.
7. **Document result**: Whether disabling/re-enabling resolved the issue.
8. **If not resolved**: Proceed to Resolution Step 5.

### Resolution Step 5: OrbitPOS v2.0 Void Bug Workaround

**This step applies only if the system is OrbitPOS v2.0 and the drawer opens randomly during void transactions.**

1. Access the **Admin Console** (**Ctrl + Alt + F12**).
2. Navigate to **System Configuration > Peripherals > Drawer**.
3. Locate the parameter **DRAWER_VOID**.
4. Change **DRAWER_VOID=1** to **DRAWER_VOID=0** and save the configuration.
5. Restart the POS system.
6. Perform a test void transaction and verify the drawer does not open.
7. **Document result**: Successfully applied v2.0 void bug workaround.
8. **Note for escalation**: Recommend upgrading to OrbitPOS v2.1 or later to resolve the underlying bug.

### Resolution Step 6: Inspect Physical Drawer Hardware

1. Using the **manual override key**, open the drawer completely and inspect the interior.
2. Check for:
   - **Loose debris** (cash, receipt fragments, foreign objects) blocking the solenoid or slide mechanism.
   - **Damaged or misaligned rails** on the sides of the drawer.
   - **Solenoid damage**: Look for corrosion, loose wires, or visible burn marks on the solenoid coil (small electromagnet on the underside of the drawer).
3. If debris is found, carefully remove it with tweezers. Do not use liquids or force.
4. If the solenoid appears damaged (burn marks, loose wires, or corrosion), **escalate to L2 immediately**—the hardware must be replaced.
5. Close the drawer firmly and test the manual open command again.
6. **Document result**: Any debris removed, any hardware damage observed.
7. **If not resolved**: Proceed to When to Escalate to L2.

---

## When to Escalate to L2

**Escalate immediately if any of the following conditions are present:**

- **Hardware damage observed**: Solenoid shows burn marks, corrosion, or loose internal wires.
- **Mechanical damage**: Drawer rails are bent, misaligned, or the drawer will not close fully even with the manual override key.
- **All L1 resolution steps have been completed** and the drawer remains unresponsive.
- **Error code `ERR_DRAWER_TIMEOUT`** persists after cable reseating and port reconfiguration.
- **Error code `DRAWER_COMM_FAIL`** indicates a serial/USB communication failure that L1 steps have not resolved.
- **Cable damage**: The drawer cable appears frayed, cut, or shows exposed wiring.
- **OrbitPOS systems**: Drawer opens randomly on void transactions even after setting **DRAWER_VOID=0** (indicates firmware bug requiring upgrade).

### Information to Collect Before Escalating

Provide L2 support with the following details:

1. **POS System**: Version number (e.g., FoodTech v5.1.2, OrbitPOS v2.0)
2. **Drawer Hardware**: Model and serial number (located on rear of drawer)
3. **Symptoms Observed**: Exact behavior (does not open, opens randomly, stuck, audible buzzing, etc.)
4. **Hardware Connection**: Which port is the drawer connected to (COM1, USB1, RJ-12, etc.)
5. **All Configuration Values**: Screenshot or list of settings from Settings > Hardware > Cash Drawer
6. **Error Messages**: Full text of any error codes (e.g., `ERR_DRAWER_TIMEOUT`, `DRAWER_COMM_FAIL`)
7. **L1 Resolution Attempts**: List all steps completed and results of each
8. **Physical Inspection Results**: Any damage, loose cables, or obstructions found

---

## Related Runbooks

- `POS_System_Startup_Troubleshooting.md`
- `FoodTech_POS_Hardware_Configuration.md`
- `OrbitPOS_Admin_Console_Access.md`
- `POS_Serial_Port_and_USB_Device_Mapping.md`
- `Cash_Drawer_Hardware_Replacement.md`
- `POS_Error_Codes_Reference.md`

---

## Revision History

| Version | Date       | Notes                                                                                               |
| ------- | ---------- | --------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for FoodTech v5.1.x; added OrbitPOS v2.0 void bug section; clarified cable reseating steps. |
| 1.1     | 2024-12-10 | Added detailed configuration steps for pulse duration adjustment.                                   |
| 1.0     | 2024-06-01 | Initial version. Covered FoodTech v4.2.x and OrbitPOS v2.x.                                         |
