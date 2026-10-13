# StarMC Print v2 Receipt Printer — Specification Sheet

## Overview

The StarMC Print v2 is a compact thermal receipt printer designed for point-of-sale (POS) and hospitality environments across ServeWell properties. This device handles high-volume receipt printing with minimal maintenance requirements and supports both wired and wireless connectivity options. The printer is integral to order fulfillment, billing, and kitchen display system (KDS) operations.

**Supported Systems:** StarMC Print v2 firmware v3.0 and above

---

## Hardware Specifications

| Specification             | Details                                       |
| ------------------------- | --------------------------------------------- |
| **Print Method**          | Direct thermal                                |
| **Print Width**           | 58mm (2.24")                                  |
| **Print Speed**           | 150mm/second (max)                            |
| **Resolution**            | 203 DPI                                       |
| **Paper Type**            | 58mm thermal receipt rolls (80×80mm standard) |
| **Paper Capacity**        | Single roll, 80×80mm or 80×150mm              |
| **Operating Temperature** | 0°C to 45°C                                   |
| **Storage Temperature**   | -20°C to 60°C                                 |
| **Power Input**           | 24V DC / 2A (via included adapter)            |
| **Connectivity**          | USB 2.0 Type-B, Bluetooth 5.0 (Class 2)       |
| **Physical Dimensions**   | 150mm (W) × 100mm (D) × 120mm (H)             |
| **Weight**                | 1.2kg (without paper)                         |
| **Warranty**              | 24 months hardware coverage                   |

---

## Software & Firmware

| Component          | Version                       | Details                                          |
| ------------------ | ----------------------------- | ------------------------------------------------ |
| **Firmware**       | v3.0+                         | Current standard across ServeWell infrastructure |
| **Compatible OS**  | Windows 7/10/11, Linux, macOS | Host system requirements                         |
| **Driver Version** | 3.2.1 (current)               | See driver download path below                   |
| **Update Policy**  | Monthly firmware patches      | Security and stability updates                   |
| **End of Support** | January 2027                  | Hardware end-of-life date                        |

### Driver Download Path

```
Internal Repository: \\servewell-repo\drivers\peripherals\StarMC_Print_v2\
Direct Link: https://support.servewell.in/downloads/starmc-print-v2-driver-3.2.1.exe
Fallback Vendor: https://starmicronics.com/downloads
```

---

## Configuration

### Default Settings

| Parameter           | Default Value    | Notes                         |
| ------------------- | ---------------- | ----------------------------- |
| **Baud Rate** (USB) | 115200           | Do not modify                 |
| **Paper Type**      | Thermal 58mm     | Configured at factory         |
| **Print Darkness**  | Level 5 (Medium) | Adjustable via driver (0-8)   |
| **Auto-cutter**     | Enabled          | Can be disabled in firmware   |
| **Bluetooth Name**  | `StarMC-XXXXX`   | Last 5 digits = serial number |
| **Bluetooth PIN**   | `0000`           | Default pairing code          |

### Key Configuration Paths

**Windows:**

```
Registry Path: HKEY_LOCAL_MACHINE\SOFTWARE\Star Micronics\StarMC Print v2
Config File: C:\ProgramData\Star Micronics\StarMC_config.ini
Driver Location: C:\Program Files\Star Micronics\StarMC Print v2 Driver
```

**Linux:**

```
Config Path: /etc/star-micronics/starmc_print_v2.conf
Log Location: /var/log/starmc_print_v2.log
```

### Bluetooth Pairing Reset Procedure

**To reset Bluetooth pairing and restore factory defaults:**

1. Power off the printer completely
2. Press and hold the **Reset Button** (small circular button on rear panel, recessed) for **10 seconds**
3. Release button when LED flashes **amber** (indicates reset mode)
4. Wait 30 seconds for reboot to complete
5. LED will return to **green** (ready state)
6. Bluetooth name resets to default: `StarMC-[XXXXX]`
7. Pairing PIN resets to: `0000`

**Re-pairing after reset:**

- On host device, remove printer from Bluetooth device list
- Search for available Bluetooth devices
- Select `StarMC-XXXXX` (matches printer serial number)
- Enter PIN when prompted: `0000`
- Connection should establish within 5 seconds

---

## Connection Options

### USB Connection

- **Cable Type:** USB 2.0 Type-B to Type-A
- **Cable Length:** 2 meters (included)
- **Installation:** Plug-and-play with driver installed
- **Advantages:** Stable, no pairing required, continuous power delivery
- **Typical Use:** Kitchen workstations, fixed POS terminals

### Bluetooth Connection

- **Pairing Range:** 10 meters (line-of-sight)
- **Supported Devices:** iOS (11+), Android (8.0+), Windows (10/11), Mac
- **Connection Stability:** Auto-reconnect if device comes within range
- **Power Requirement:** Printer must be plugged in; Bluetooth does not operate on battery
- **Typical Use:** Mobile POS, tablet ordering systems, temporary workstations

---

## Error Codes & LED Indicators

### LED Status Codes

| LED Color            | Status                           | Action Required                       |
| -------------------- | -------------------------------- | ------------------------------------- |
| **Green (solid)**    | Ready/Normal operation           | None                                  |
| **Green (blinking)** | Printing in progress             | None                                  |
| **Amber (solid)**    | Warming up or calibrating        | Wait 10-15 seconds                    |
| **Amber (blinking)** | Paper low or nearly empty        | Replace paper roll soon               |
| **Red (solid)**      | Error state—see error code table | Check error code, troubleshoot        |
| **Red (blinking)**   | Critical hardware failure        | Do not attempt repair; escalate to L2 |
| **Off**              | No power or power failure        | Check power adapter and connection    |

### Error Codes & Messages

| Error Code | LED Pattern    | Meaning                    | L1 Resolution                                          |
| ---------- | -------------- | -------------------------- | ------------------------------------------------------ |
| **E001**   | Red, 1 flash   | Paper out                  | Load new thermal paper roll (58mm)                     |
| **E002**   | Red, 2 flashes | Paper jam                  | Open access door, remove jammed paper, close door      |
| **E003**   | Red, 3 flashes | Cutter malfunction         | Power cycle printer; if persists, escalate             |
| **E004**   | Red, 4 flashes | Thermal head error         | Power off 2 min, check for debris, power on            |
| **E005**   | Red, 5 flashes | Firmware corrupted         | Contact L2 for firmware re-flash                       |
| **E010**   | Red, solid     | Temperature sensor failure | Do not operate; escalate to L2                         |
| **E015**   | Red, solid     | Bluetooth pairing lost     | Restart Bluetooth on host device; re-pair if needed    |
| **E020**   | Red, blinking  | Power supply failure       | Check adapter connection; replace adapter if necessary |

### Common Troubleshooting Steps

**Issue: Printer not printing after job sent**

1. Check USB/Bluetooth connection status
2. Verify paper is loaded and not jammed
3. Restart printer (power cycle)
4. Reinstall driver if USB connection fails

**Issue: Poor print quality (faint text)**

1. Adjust print darkness in driver settings (increase to Level 6-7)
2. Check that thermal paper is not expired (1-2 year shelf life)
3. Clean thermal head with dry, lint-free cloth

**Issue: Bluetooth repeatedly disconnects**

1. Perform Bluetooth pairing reset (see Configuration section)
2. Ensure no physical obstructions between printer and host device
3. Move printer closer to host device (within 5 meters)
4. Check for interference from other 2.4GHz devices (WiFi, cordless phones)

---

## Maintenance & Care

| Task                         | Frequency | Instructions                                              |
| ---------------------------- | --------- | --------------------------------------------------------- |
| **Paper Roll Inspection**    | Daily     | Check for tears, dust, or damage                          |
| **Thermal Head Cleaning**    | Weekly    | Use provided cleaning cloth; never use water              |
| **Power Adapter Check**      | Monthly   | Verify no fraying, overheating, or loose connections      |
| **Firmware Update Check**    | Monthly   | Check servewell.in support portal for patches             |
| **Full Hardware Inspection** | Quarterly | Check for physical damage, loose connectors, dust buildup |

---

## Support & Escalation

| Contact                             | Details                                            | Availability                                        |
| ----------------------------------- | -------------------------------------------------- | --------------------------------------------------- |
| **L1 Support**                      | Internal ticketing system (Jira)                   | 24/7                                                |
| **L2 Support**                      | it-l2@servewell.in                                 | 8:00 AM – 8:00 PM IST, Mon-Sat                      |
| **Vendor Support (Star Micronics)** | support@starmicronics.com                          | Business hours, US timezone                         |
| **Hardware Replacement**            | facilities-logistics@servewell.in                  | Request within 24 hours of failure                  |
| **Escalation Threshold**            | Error codes E010, E005, E020, or repeated failures | Do not attempt repair; submit L2 ticket immediately |

### Information to Include in Support Tickets

- Printer serial number (on rear panel)
- Current firmware version (check in printer settings)
- Error code(s) and LED pattern observed
- Connection type (USB or Bluetooth)
- Host device OS and version
- Steps already attempted

---

## Revision History

| Version | Date           | Author                     | Notes                                                                                             |
| ------- | -------------- | -------------------------- | ------------------------------------------------------------------------------------------------- |
| 1.0     | 2025-01-15     | IT Knowledge Base Team     | Initial specification sheet for StarMC Print v2 v3.0                                              |
| 1.1     | 2025-06-20     | IT Knowledge Base Team     | Added Bluetooth pairing reset procedure; updated error code table                                 |
| 1.2     | 2025-08-01     | IT Knowledge Base Team     | Clarified paper type specifications; added maintenance schedule; expanded troubleshooting section |
| **1.3** | **2025-12-10** | **IT Knowledge Base Team** | **Current version—driver updated to 3.2.1; added connection options section**                     |

---

**Document Classification:** Internal Use — L1 Support Reference  
**Last Updated:** December 10, 2025  
**Next Review Date:** March 10, 2026
