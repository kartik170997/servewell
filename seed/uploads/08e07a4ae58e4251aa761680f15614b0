# POS Barcode Scanner Not Reading

## Overview

A barcode or QR code scanner connected to a FoodTech POS terminal is not reading items, producing beeps without registering scans, or is not recognized by the system. This runbook covers USB and Bluetooth Honeywell and Zebra scanner models commonly deployed in ServeWell locations.

## Affected Systems

- **POS Software:** FoodTech POS v4.2.x, v5.1.x
- **Scanner Models:**
  - Honeywell Voyager 1472g (USB/Bluetooth)
  - Honeywell Granit 1981i (Bluetooth)
  - Zebra DS3678-HP (Bluetooth)
  - Zebra DS4308 (USB)
- **Connection Types:** USB wired, Bluetooth wireless

## Symptoms

- Scanner is powered on but does not register barcode/QR scans
- Scanner beeps (indicating successful scan) but no data appears in POS system
- Scanner appears in Windows Device Manager but not recognized by FoodTech POS
- Bluetooth scanner fails to pair or frequently disconnects
- "Scanner Not Found" error message in POS Item Lookup screen
- Partial or corrupted scan data (e.g., only first 3 digits of barcode appear)

## Immediate Steps (First 2 Minutes)

**For Store Staff Before Calling IT:**

1. **Power cycle the scanner:**
   - Power off the scanner using the power button (hold 3 seconds on Bluetooth models).
   - Wait 10 seconds.
   - Power on and attempt to scan a known item (e.g., a beverage bottle with a clear barcode).

2. **Verify scanner is in the correct mode:**
   - For USB scanners: Ensure the USB cable is firmly seated in both the scanner and the POS terminal.
   - For Bluetooth scanners: Ensure the scanner displays a blue LED indicator (not red or amber).

3. **Test with a different barcode:**
   - Attempt to scan 2–3 different items with clear, undamaged barcodes.
   - If some barcodes scan and others don't, the issue may be barcode quality, not the scanner.

---

## L1 Diagnosis Steps

### Step 1: Confirm Scanner Hardware Status

1. Ask store staff: **"Is the scanner powered on? What color is the LED indicator?"**
   - **Expected:** Steady green (USB) or steady/blinking blue (Bluetooth).
   - **Issue indicators:** Red, amber, or no light = power/connectivity problem.

2. For **USB scanners:**
   - Visually inspect the USB cable for damage, kinks, or loose connectors.
   - Try a different USB port on the POS terminal (avoid USB hubs if possible).
   - Document the USB port used (e.g., "Port 3 on back of terminal").

3. For **Bluetooth scanners:**
   - Check the scanner's battery level (press the battery indicator button; should show green LEDs).
   - If battery is low (amber/red), ask staff to charge the scanner for 30 minutes before proceeding.

### Step 2: Check Device Manager Registration

1. **Remote into the affected POS terminal** using your standard remote access tool (e.g., TeamViewer, AnyDesk).

2. **Open Device Manager:**
   - Windows 10/11: Press `Win + X` → select **Device Manager**.
   - Or: Search "Device Manager" in Start menu.

3. **For USB scanners:**
   - Expand **Human Interface Devices**.
   - Look for your scanner model name (e.g., "Honeywell Voyager 1472g" or "Zebra DS4308").
   - **Expected:** Device listed with a green checkmark and no warning icons.
   - **Issue:** Device not listed, or listed under "Other Devices" with a yellow warning triangle.

4. **For Bluetooth scanners:**
   - Expand **Bluetooth**.
   - Look for the scanner device name (e.g., "Honeywell Granit 1981i").
   - **Expected:** Status shows "Connected".
   - **Issue:** Status shows "Paired" but not "Connected", or device missing entirely.

**Document the exact device name and status for escalation if needed.**

### Step 3: Verify FoodTech POS Scanner Configuration

1. **Launch FoodTech POS** (if not already running).

2. **Navigate to Settings/Configuration:**
   - Click **Admin** (or **Settings** depending on v4.2.x vs. v5.1.x).
   - Select **Hardware Configuration** or **Peripherals**.
   - Locate **Scanner Settings** or **Barcode Reader**.

3. **For FoodTech POS v4.2.x:**
   - Check **Active Scanner Device** dropdown. Confirm the correct scanner model is selected.
   - Note the COM port (USB scanners often use COM3–COM6) or Bluetooth device name.

4. **For FoodTech POS v5.1.x:**
   - Check **Scanner Interface** setting (USB or Bluetooth).
   - Verify **Scanner Model** matches the physical device (Honeywell vs. Zebra).
   - Confirm **Scanner Enabled** is set to **Yes/True**.

5. **Note any error codes displayed** (e.g., "ERR-SCAN-001: Device not found").

**Document the current configuration setting and any error codes.**

### Step 4: Test Scanner in FoodTech POS

1. In the POS main screen, navigate to **Item Lookup** or **Quick Scan** screen.

2. **Place cursor in the barcode input field** (usually indicated by a cursor or focus rectangle).

3. **Scan a known item** (e.g., a house wine bottle, branded snack, or beverage with a clear UPC).

4. **Observe the result:**
   - **Success:** Barcode appears in the field and item details populate.
   - **Partial read:** Only first few digits appear; scan cuts off mid-barcode.
   - **No response:** Scanner beeps but no data in POS.
   - **Slow response:** Data appears 2–3 seconds after scan (may indicate slow USB/Bluetooth connection).

**Document what happens during the test scan, including any beeps or error messages on the POS screen.**

### Step 5: Check Scanner Driver Version

1. **For USB scanners:**
   - In Device Manager, right-click the scanner device → **Properties**.
   - Go to **Details** tab.
   - Select **Driver Version** from the dropdown menu.
   - **Expected driver:** v2.x or later for Honeywell; v1.5.x or later for Zebra.
   - **Action:** If driver is older than 2 years, note for potential update.

2. **For Bluetooth scanners:**
   - Bluetooth drivers are typically managed by Windows or the terminal manufacturer.
   - Check **Device Manager > Bluetooth** for any warning icons.
   - If available, launch the **Honeywell Bluetooth Scanner Utility** or **Zebra DataWedge** software to check firmware version.

---

## L1 Resolution

### **Resolution Path 1: USB Scanner Not Detected**

1. **Disconnect the USB cable** from both the scanner and the POS terminal.

2. **Wait 30 seconds** for Windows to release the device driver.

3. **Reconnect the USB cable firmly** to the POS terminal.
   - Try a different USB port if the original port shows issues in Device Manager.
   - **Avoid USB hubs**—connect directly to the terminal's USB port.

4. **Wait 10–15 seconds** for Windows to detect and install the driver automatically.

5. **Verify in Device Manager:**
   - Device should appear under **Human Interface Devices** with a green checkmark.
   - No yellow warning triangles.

6. **Test in FoodTech POS:**
   - Restart FoodTech POS completely (close and reopen the application).
   - Attempt to scan an item.
   - **Expected:** Barcode registers in Item Lookup screen.

7. **If resolved:** Document the solution in the ticket and close.

---

### **Resolution Path 2: Bluetooth Scanner Pairing Issue**

1. **On the POS terminal, open Bluetooth Settings:**
   - Windows 10/11: **Settings > Devices > Bluetooth & other devices**.

2. **If the scanner appears in the paired devices list:**
   - Click the scanner name.
   - Select **Remove device** or **Forget**.
   - Wait 5 seconds.

3. **Power off the Bluetooth scanner** (hold power button 3 seconds) and remove the battery for 10 seconds.

4. **Reinsert the battery and power on the scanner.**
   - Scanner should enter pairing mode (LED will blink blue rapidly).

5. **On the POS terminal, click "Add device"** or **"Pair a new device"** in Bluetooth Settings.

6. **Select the scanner from the available devices list** (e.g., "Honeywell Granit 1981i").

7. **Complete the pairing process:**
   - Accept any PIN prompts (default PIN is usually `0000` or `1234` for ServeWell devices).
   - Wait for status to show **"Connected"** (not just "Paired").

8. **Verify in FoodTech POS:**
   - Open **Admin > Hardware Configuration > Scanner Settings**.
   - Confirm the Bluetooth scanner is now listed as **Active** and **Connected**.
   - Test by scanning an item.

9. **If resolved:** Document the pairing procedure completed and close the ticket.

---

### **Resolution Path 3: Scanner Recognized But Not Reading (FoodTech Configuration Issue)**

1. **Open FoodTech POS and navigate to Admin > Hardware Configuration > Scanner Settings.**

2. **Verify the Scanner Enabled setting:**
   - **For v4.2.x:** Check that **Scanner Active** is set to **Yes**.
   - **For v5.1.x:** Check that **Scanner Enabled** is toggled **On/True**.

3. **If disabled, enable the scanner:**
   - Click **Yes** (v4.2.x) or toggle **On** (v5.1.x).
   - Click **Save** or **Apply** (button location varies by version).

4. **Restart FoodTech POS:**
   - Close the application completely (File > Exit or the X button).
   - Wait 5 seconds.
   - Relaunch FoodTech POS.

5. **Test a scan:**
   - Go to **Item Lookup** or **Quick Scan**.
   - Scan a known item.
   - **Expected:** Barcode and item details appear.

6. **If resolved:** Document that scanner was disabled in configuration and has been re-enabled. Close the ticket.

---

### **Resolution Path 4: Partial or Corrupted Barcode Reads**

1. **Test with multiple barcodes:**
   - Scan 5 different items with clear, undamaged barcodes.
   - **If 4 out of 5 read correctly:** The issue is likely barcode quality, not the scanner.
   - **If all barcodes read partially:** Proceed to step 2.

2. **Check scanner decode settings:**
   - Open FoodTech POS **Admin > Hardware Configuration > Scanner Settings**.
   - Look for **Barcode Decode Mode** or **Scanner Type**.
   - Verify the setting matches the barcode types in use (e.g., "Code 128", "UPC", "EAN", "QR Code").
   - **For Honeywell scanners:** Confirm **Wedge Mode** is enabled (usually the default).

3. **If an incorrect decode mode is selected:**
   - Change the setting to match your barcode types (e.g., "Auto-Detect" if available).
   - Click **Save** and restart FoodTech POS.
   - Test with a known barcode.

4. **Check barcode quality:**
   - Visually inspect the barcodes being scanned for damage, dirt, or fading.
   - Clean the barcode with a dry cloth if necessary.
   - Attempt to scan again.

5. **If issue persists after 5 test scans, escalate to L2** with documentation of which barcodes read completely vs. partially.

---

## When to Escalate to L2

**Escalate to L2 Support if any of the following conditions are met:**

1. **Scanner remains undetected in Device Manager after reconnection:**
   - The device does not appear under **Human Interface Devices** or **Bluetooth** after two reconnection attempts.
   - A yellow warning triangle persists next to the device name.
   - **Information to include:** Screenshot of Device Manager, USB port used, scanner model and serial number.

2. **Bluetooth pairing fails or cannot be completed:**
   - The scanner does not appear in the available Bluetooth devices list after 3 pairing attempts.
   - Pairing completes but status shows "Paired" (not "Connected") and remains disconnected after 5 minutes.
   - **Information to include:** Scanner model, POS terminal model, Bluetooth adapter model (if external).

3. **FoodTech POS does not recognize the scanner even after configuration changes:**
   - Scanner is detected in Device Manager but still shows "Device Not Found" or "ERR-SCAN-001" in FoodTech POS.
   - A different scanner of the same model works on another terminal (cross-device test).
   - **Information to include:** FoodTech POS version, exact error code, scanner serial number.

4. **Barcode reads are consistently corrupted or incomplete across multiple barcodes:**
   - More than 50% of scan attempts result in partial reads after confirming barcode quality.
   - Issue occurs on multiple barcodes but resolves when using a backup scanner (indicating hardware failure).
   - **Information to include:** Examples of corrupted reads, number of test scans performed, backup scanner model (if tested).

5. **Scanner beeps but produces no output in FoodTech POS after all L1 troubleshooting:**
   - The scanner beeps audibly on each scan attempt, but no barcode data appears in POS after restarting the application and reconnecting the device.
   - The issue has persisted for more than 30 minutes and is impacting business operations.
   - **Information to include:** Symptom timeline, any recent updates to POS software or Windows, detailed description of beep pattern (single beep vs. multi-beep).

**Before escalating, collect and attach the following documentation:**

- Screenshots of Device Manager (Devices tab showing scanner status)
- Screenshots of FoodTech POS **Admin > Hardware Configuration > Scanner Settings** page
- Description of troubleshooting steps already attempted
- Scanner model, serial number, and firmware version (if available)
- POS terminal model and Windows OS version
- Any error codes or messages observed during diagnosis

---

## Related Runbooks

- `FoodTech_POS_Initial_Setup.md`
- `USB_Device_Driver_Installation.md`
- `Bluetooth_Pairing_Troubleshooting.md`
- `FoodTech_POS_Hardware_Configuration.md`
- `Windows_Device_Manager_Guide.md`
- `Honeywell_Voyager_1472g_Setup.md`
- `Zebra_DS4308_Pairing_Guide.md`

---

## Revision History

| Version | Date       | Notes                                                                                         |
| ------- | ---------- | --------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for FoodTech POS v5.1.x; added Bluetooth pairing specifics; enhanced diagnostic steps |
| 1.1     | 2024-11-20 | Added resolution paths; clarified Device Manager navigation for Windows 10/11                 |
| 1.0     | 2024-06-01 | Initial version; covered v4.2.x and USB scanner basics                                        |
