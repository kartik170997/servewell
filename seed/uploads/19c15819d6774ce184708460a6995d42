# Printer Driver Reinstall Procedure

## Overview

This runbook provides step-by-step instructions for diagnosing and resolving corrupted, missing, or incompatible printer drivers on EpsonTM-T88VI v1.12 and StarMC Print v2 v3.0 devices running Windows 10. Driver issues commonly occur after Windows updates and require clean uninstallation followed by reinstallation of manufacturer-specific drivers.

## Affected Systems

- **Printer Models**: EpsonTM-T88VI v1.12, StarMC Print v2 v3.0
- **Operating System**: Windows 10 (all current versions)
- **Common Trigger**: Windows Update installations and cumulative security patches
- **Scope**: ServeWell Hospitality POS terminals, kitchen prep stations, and front-of-house receipt printers

## Symptoms

- Printer shows as "Unknown Device" or "Other Devices" in Device Manager
- Print jobs remain in queue indefinitely without printing
- Error message: "Driver not installed" or "No compatible driver found"
- Printer appears offline in Windows despite USB/network connectivity
- Applications (POS software, kitchen display systems) cannot communicate with printer
- Device Manager displays yellow exclamation mark (!) or red X on printer entry
- Error Code 10, 43, or 45 in Device Properties
- Printer tests fail in Windows Settings > Devices > Printers & Scanners
- Generic Windows drivers installed, causing functionality loss (no specialty features, thermal settings unavailable)

## Immediate Steps (First 2 Minutes)

Store staff or first responder can perform these quick checks:

1. **Verify Physical Connection**
   - For USB printers: Check that the cable is fully inserted into both the printer and the Windows 10 device
   - For network printers: Confirm the printer has network connectivity (check LED indicators on printer front panel)
   - Restart both the printer and the Windows device (power off 30 seconds, power on)

2. **Check Print Queue**
   - On Windows 10 device, press **Windows Key + I** to open Settings
   - Navigate to **Devices > Printers & Scanners**
   - Locate the printer name and select it
   - Click **Open queue** and cancel any stuck print jobs

3. **Verify Printer Power and Network Status**
   - Ensure printer is powered on and fully booted (check LED indicators)
   - For network printers, verify network cable is connected or WiFi is enabled

If these steps do not resolve the issue, proceed to L1 Diagnosis.

## L1 Diagnosis Steps

Perform the following diagnostic steps in order. Document findings for potential escalation.

### Step 1: Verify Device Manager Detection

1. Right-click the **Start Menu** and select **Device Manager**
2. Locate the printer in the device tree (check under **Printers**, **Other Devices**, or **Universal Serial Bus Controllers**)
3. **Document the exact device name and any error codes** displayed
4. If not visible, the printer may not be detected by Windows at all; escalate to L2 if USB connection is confirmed working

### Step 2: Check Current Driver Status

1. In Device Manager, right-click the printer device
2. Select **Properties** and navigate to the **Driver** tab
3. Note the **Driver Provider** field:
   - If it shows "Microsoft" or "Windows Update", a generic driver is installed (problematic—proceed to resolution)
   - If it shows "Epson" or "Star Micronics", a manufacturer driver may be present but corrupted
4. Click **Driver Details** and document the driver file path (usually `C:\Windows\System32\drivers\...`)
5. Check the **Driver Version** number and **Date** published

### Step 3: Verify Internet/SharePoint Access

1. On the affected Windows 10 device, open a web browser
2. Navigate to the internal SharePoint driver repository: `https://sharepoint.servewell.local/drivers`
3. Confirm you can access the folder without authentication errors
4. If access is denied, note the error message and escalate

### Step 4: Test Printer Connectivity

1. On Windows 10 device, press **Windows Key + I** to open Settings
2. Go to **Devices > Printers & Scanners**
3. Select the printer and click **Open queue**
4. Attempt to print a test page (if available button is present)
5. **Document any error messages** that appear

### Step 5: Check for Known Conflicts

1. Open Device Manager again
2. Expand **Universal Serial Bus Controllers**
3. Look for any devices with yellow warning icons
4. Check **View > Show Hidden Devices** to reveal disconnected/phantom devices
5. Document any suspicious entries related to printers or serial devices

## L1 Resolution

Follow these steps **in order** to reinstall the correct driver. **Do not skip the clean uninstall step.**

### Resolution A: EpsonTM-T88VI v1.12 Driver Reinstall

#### Phase 1: Clean Uninstall (Mandatory)

1. **Disconnect the printer**
   - Power off the EpsonTM-T88VI physically
   - Disconnect the USB cable from the Windows 10 device (wait 30 seconds)

2. **Uninstall via Device Manager**
   - Press **Windows Key + X** and select **Device Manager**
   - Locate the Epson printer (check **Printers**, **Other Devices**, **USB Devices**)
   - Right-click the device and select **Uninstall device**
   - Check the box: **"Delete the driver software for this device"**
   - Click **Uninstall** and wait for completion (may take 1–2 minutes)

3. **Remove Registry Entries (Optional but Recommended)**
   - Press **Windows Key + R**, type `regedit`, and press **Enter**
   - Navigate to: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services`
   - Search for any keys starting with "usbprint" or "epson"
   - Right-click and **Delete** if found (note: do not delete system critical entries)
   - Close Registry Editor

4. **Restart Windows Device**
   - Restart the Windows 10 device and allow full boot (2–3 minutes)
   - Do not reconnect printer until restart is complete

#### Phase 2: Driver Download

5. **Access SharePoint Driver Repository**
   - Open a web browser and navigate to: `https://sharepoint.servewell.local/drivers`
   - Locate folder: **EpsonTM-T88VI > v1.12 > Windows10**
   - Download file: **EpsonTM-T88VI_v1.12_Win10_Driver.exe** (approximately 45–65 MB)
   - Save to a known location (e.g., **C:\Drivers** or Desktop)
   - **Verify file integrity**: Check that file size matches SharePoint listing (if size mismatch, re-download)

#### Phase 3: Driver Installation

6. **Run Installation Executable**
   - Double-click **EpsonTM-T88VI_v1.12_Win10_Driver.exe**
   - If prompted by User Account Control, click **Yes** to allow
   - The Epson installer window will open; click **Next >**
   - Agree to the license agreement and click **Next >**
   - Select installation path (default: `C:\Program Files\Epson\...`) and click **Next >**
   - Choose **Standard Installation** (do not select Custom unless troubleshooting specific issues)
   - Click **Install** and wait for completion (3–5 minutes)
   - When prompted, click **Finish**

7. **Reconnect Printer**
   - Power on the EpsonTM-T88VI
   - Connect the USB cable to the Windows 10 device
   - Windows will detect the device; allow 1–2 minutes for driver binding

8. **Verify Installation**
   - Open Device Manager
   - Expand **Printers** and confirm **"EpsonTM-T88VI"** appears **without error icons**
   - Right-click and select **Properties > Driver tab**
   - Confirm **Driver Provider** shows **"Epson"** and version matches downloaded file (v1.12 or later)

#### Phase 4: Functional Testing

9. **Test Print Functionality**
   - Press **Windows Key + I** and go to **Devices > Printers & Scanners**
   - Select **EpsonTM-T88VI** and click **Open queue**
   - Click **Printer > Print Test Page** (if available)
   - Verify receipt paper prints without errors
   - If successful, document completion and close

---

### Resolution B: StarMC Print v2 v3.0 Driver Reinstall

#### Phase 1: Clean Uninstall (Mandatory)

1. **Disconnect the printer**
   - Power off the Star Micronics printer
   - Disconnect USB or network cable from Windows 10 device

2. **Uninstall via Settings (Preferred Method)**
   - Press **Windows Key + I** to open **Settings**
   - Go to **Apps > Apps & features**
   - Search for **"Star"** or **"StarMC Print"**
   - Click the application name and select **Uninstall**
   - Follow on-screen prompts and confirm uninstall
   - Click **Yes** if prompted to restart

3. **Uninstall via Device Manager (Secondary)**
   - If app uninstall above does not fully remove driver:
   - Press **Windows Key + X** and select **Device Manager**
   - Locate Star Micronics printer (check **Printers**, **Other Devices**)
   - Right-click and select **Uninstall device**
   - Check **"Delete the driver software for this device"**
   - Click **Uninstall**

4. **Restart Windows Device**
   - Restart the Windows 10 device (do not reconnect printer yet)

#### Phase 2: Driver Download

5. **Access SharePoint Driver Repository**
   - Open web browser: `https://sharepoint.servewell.local/drivers`
   - Navigate to folder: **StarMC > PrintV2 > v3.0 > Windows10**
   - Download: **StarMC_Print_v2_v3.0_Win10_Driver.zip** (approximately 30–50 MB)
   - Save to **C:\Drivers** or Desktop
   - **Right-click the .zip file > Extract All > Extract**
   - Note the extracted folder path (e.g., `C:\Drivers\StarMC_Print_v2_v3.0_Win10_Driver\`)

#### Phase 3: Driver Installation

6. **Run Installation from Extracted Folder**
   - Open the extracted folder
   - Locate and double-click **Setup.exe** (or **StarMC_Install.exe**)
   - If User Account Control prompt appears, click **Yes**
   - The Star Micronics installer wizard will launch; click **Next >**
   - Read and accept the license terms; click **Next >**
   - Choose standard installation directory and click **Next >**
   - Confirm **"Install print driver"** is checked
   - Click **Install** and wait for completion (2–4 minutes)
   - Click **Finish** when installation completes

7. **Reconnect Printer**
   - Power on the Star Micronics printer
   - Reconnect USB cable (or confirm network connection if network-based)
   - Windows will detect and bind driver automatically (allow 1–2 minutes)

8. **Verify Installation**
   - Press **Windows Key + I** and navigate to **Devices > Printers & Scanners**
   - Locate **"Star Micronics Print"** or device model name (e.g., "Star MC3042")
   - Confirm printer shows **Ready** status (no error symbols)
   - Right-click and select **Printer properties**
   - Navigate to **Advanced** tab and verify **Driver Name** contains "Star" (not "Generic")

#### Phase 4: Functional Testing

9. **Test Print Functionality**
   - In **Printers & Scanners**, right-click the Star printer and select **Open queue**
   - Send a test print job from a POS application or use **Print Test Page**
   - Verify output prints correctly with proper formatting and no garbled text
   - Document successful completion

---

## When to Escalate to L2

Escalate the ticket to L2 Support (Remote Desktop/On-Site) if **any** of the following conditions are met:

### Escalation Criteria

1. **Driver File Corruption or Missing**
   - SharePoint driver file is inaccessible, corrupted, or version mismatch occurs
   - Downloaded .exe or .zip file fails hash validation or will not extract/run
   - **Information to collect**: File size, modification date, error message, user account used

2. **Device Manager Detection Failure**
   - Printer does not appear in Device Manager even after disconnect/reconnect
   - USB device appears as "Unknown Device" with Error Code 43 or 45 after installation attempt
   - Network printer does not appear in network device list
   - **Information to collect**: Device Manager screenshot, exact error code, USB port tested, network configuration

3. **Installation Failure**
   - Setup.exe or installer crashes with error code (document the code)
   - Installer requests missing files or dependencies
   - Installation completes but driver does not bind to hardware
   - **Information to collect**: Complete error message, installer log file (if available), Windows 10 build number

4. **Post-Installation Issues**
   - Printer appears in Device Manager but remains offline or unavailable in POS system
   - Print test page fails even after successful driver installation
   - POS application reports "Printer not found" or "Unable to initialize"
   - Error Code 10 persists after clean reinstall
   - **Information to collect**: Device Manager Properties screenshot, POS error log, Windows Event Viewer errors

5. **Persistent Hardware Issues**
   - USB connection fails on multiple ports (hardware defect suspected)
   - Printer firmware is outdated and requires firmware update (beyond L1 scope)
   - Printer is physically damaged or non-responsive
   - **Information to collect**: Hardware diagnostics, printer self-test results (if available)

6. **System-Level Conflicts**
   - Multiple yellow warning icons in Device Manager related to USB or serial devices
   - Windows Update is blocking driver installation or rolling back changes
   - Antivirus or security software is quarantining driver files
   - **Information to collect**: Windows Update history, Antivirus quarantine log, full Device Manager list

### Information to Collect Before Escalation

Document the following details in the ticket before assigning to L2:

- **Device Hostname/Asset ID**: Exact Windows 10 computer name
- **Printer Model & Serial Number**: Physical label information from printer
- **Windows 10 Build Number**: From **Settings > System > About**
- **Driver Installation Attempt**: Version attempted, date/time, error messages
- **Screenshots**: Device Manager Properties, Printers & Scanners, any error dialogs
- **Connectivity Method**: USB port number, network IP (if applicable)
- **Recent Changes**: Recent Windows updates, POS software updates, hardware replacements
- **Reproduction Steps**: Exact steps to reproduce the issue
- **Impact Scope**: Single device or multiple devices affected?

---

## Related Runbooks

- `Printer-Network-Configuration.md` — Configuring network printers and IP assignment
- `Printer-USB-Connection-Troubleshooting.md` — Diagnosing USB connectivity and port issues
- `Windows-Device-Manager-Errors.md` — Understanding and resolving Device Manager error codes
- `POS-System-Printer-Integration.md` — Validating printer availability in POS applications
- `Windows-10-Update-Compatibility.md` — Preparing systems for Windows updates without driver loss
- `Epson-TM-T88VI-Maintenance.md` — Hardware maintenance and firmware updates
- `Star-Micronics-Print-V2-Settings.md` — Advanced driver configuration and print settings

---

## Revision History

| Version | Date       | Notes                                                                                                |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for current system versions; clarified escalation criteria; added Phase 4 functional testing |
| 1.1     | 2024-12-10 | Added registry cleanup step; included specific SharePoint paths; expanded escalation troubleshooting |
| 1.0     | 2024-06-01 | Initial version; basic driver reinstall procedure                                                    |

---

**Document Owner**: ServeWell Hospitality IT Help Desk  
**Last Updated**: September 15, 2025  
**Next Review**: September 15, 2026
