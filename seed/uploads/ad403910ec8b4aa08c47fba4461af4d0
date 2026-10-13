# EpsonTM-T88VI Receipt Printer — Specification Sheet

## Overview

The EpsonTM-T88VI is a high-performance thermal receipt printer designed for point-of-sale (POS) and hospitality environments. It serves as a critical component in ServeWell's transaction processing infrastructure, printing itemized receipts, kitchen orders, and customer confirmations across all venue locations. The printer operates silently with minimal maintenance requirements, making it ideal for front-of-house and back-of-kitchen deployment.

---

## Hardware Specifications

| Specification             | Details                                    |
| ------------------------- | ------------------------------------------ |
| **Model**                 | EpsonTM-T88VI v1.12                        |
| **Print Method**          | Thermal line printing                      |
| **Print Width**           | 80mm (3.15")                               |
| **Print Speed**           | Up to 500mm/second                         |
| **Resolution**            | 203 DPI (8 dots/mm)                        |
| **Processor**             | 32-bit RISC Processor                      |
| **Memory (RAM)**          | 8MB SDRAM / 2MB Flash ROM                  |
| **Paper Capacity**        | Roll (80mm x 80mm, up to 40 rolls per box) |
| **Paper Type**            | 80mm thermal paper, BPA-free, 55-80gsm     |
| **Power Supply**          | External AC adapter, 100-240V, 50/60Hz     |
| **Power Consumption**     | 45W (operating), 3W (standby)              |
| **Operating Temperature** | 0°C to 45°C                                |
| **Storage Temperature**   | -20°C to 60°C                              |
| **Dimensions**            | 210(W) x 152(D) x 145(H) mm                |
| **Weight**                | 3.6 kg                                     |

---

## Connectivity Options

| Interface           | Details                          | Default   |
| ------------------- | -------------------------------- | --------- |
| **USB**             | USB 2.0 Type B, 480 Mbps         | Primary   |
| **Ethernet**        | RJ-45, 10/100 Base-TX, TCP/IP    | Secondary |
| **Serial (RS-232)** | DB-9 connector, 9600-115200 baud | Tertiary  |

---

## Software & Firmware

| Component            | Version   | Details                                   |
| -------------------- | --------- | ----------------------------------------- |
| **Firmware**         | v1.12     | Current stable release                    |
| **Driver (Windows)** | 2.12.7    | See download path below                   |
| **Driver (Linux)**   | 2.12.7    | CUPS-compatible                           |
| **Driver (macOS)**   | 2.12.6    | macOS 10.14+                              |
| **Update Policy**    | Quarterly | Automatic via WSUS (Windows environments) |

### Driver Download Path

- **Internal Repository:** `\\servewell-repo\drivers\Epson\TM-T88VI\v2.12.7\`
- **Vendor Portal:** https://www.epson.com/cgi-bin/Store/support/supportsearch.jsp
- **Alternative:** Contact IT-L2 for driver distribution package

---

## Configuration

### Default Settings

| Parameter                 | Default Value    | Modifiable |
| ------------------------- | ---------------- | ---------- |
| **Baud Rate (Serial)**    | 9600             | Yes        |
| **IP Address (Ethernet)** | DHCP enabled     | Yes        |
| **Paper Width Detection** | Auto             | Yes        |
| **Print Darkness**        | Level 5 (Medium) | Yes        |
| **Font**                  | ASCII (12x24)    | Yes        |
| **Character Code**        | Page 437 (USA)   | Yes        |
| **Auto-cutter**           | Enabled          | Yes        |

### Configuration File Paths

- **Windows:** `C:\ProgramData\Epson\TM-T88VI\config.ini`
- **Linux/CUPS:** `/etc/cups/ppd/Epson_TM-T88VI.ppd`
- **Network Settings:** Accessible via thermal receipt printer's web interface (IP-based models)

### Network Configuration (Ethernet Models)

1. Obtain printer's IP via DHCP or assign static IP
2. Access web interface: `http://<printer-ip>/`
3. Default credentials: `admin` / `epson` (change immediately)
4. Configure network parameters: gateway, DNS, SSID (optional Wi-Fi)

---

## Error Codes & Indicators

### LED Status Indicators

| LED Color  | Status   | Meaning                        | Action                                     |
| ---------- | -------- | ------------------------------ | ------------------------------------------ |
| **Green**  | Solid    | Ready to print                 | No action needed                           |
| **Green**  | Blinking | Processing/Printing            | Wait for completion                        |
| **Orange** | Solid    | Paper low                      | Replace paper roll soon                    |
| **Orange** | Blinking | Waiting for network connection | Check network cable (Ethernet models)      |
| **Red**    | Solid    | Error condition                | See error codes below; power cycle printer |
| **Red**    | Blinking | Critical hardware failure      | Contact vendor support immediately         |

### Common Error Codes

| Code    | LED Pattern   | Meaning                | Resolution                                            |
| ------- | ------------- | ---------------------- | ----------------------------------------------------- |
| **E-1** | 1 red flash   | Cover open             | Close the printer access cover and press power button |
| **E-2** | 2 red flashes | Paper end              | Install new 80mm thermal paper roll                   |
| **E-3** | 3 red flashes | Paper jam              | Open cover, remove jammed paper, close and reset      |
| **E-4** | 4 red flashes | Cutter error           | Press power button twice; if persists, escalate to L2 |
| **E-5** | 5 red flashes | High temperature error | Turn off printer, allow 10min cooldown, restart       |
| **E-6** | 6 red flashes | Firmware corruption    | Perform firmware reset (see self-test steps)          |
| **E-7** | 7 red flashes | Memory error           | Power cycle; contact IT-L2 if error repeats           |

---

## Self-Test Print Steps

### Method 1: Hardware Self-Test (Recommended for L1)

1. **Power off** the printer completely (wait 5 seconds)
2. **Ensure paper is loaded** (80mm thermal roll, BPA-free)
3. **Press and hold** the power button for **3 seconds** while powering on
4. **Release** when the LED flashes green
5. Printer will automatically print a **self-test page** showing:
   - Firmware version and serial number
   - Print quality sample (bitmap test pattern)
   - Sensor status report
   - Memory test results
6. **Verify output**: Test page should print clearly without gaps or streaks
7. If successful, LED returns to solid green; printer is operational
8. If failed, note the error code and contact IT-L2

### Method 2: Software Self-Test (Windows Driver)

1. Navigate to **Control Panel** → **Devices and Printers**
2. Right-click **Epson TM-T88VI** → **Printer Properties**
3. Select **Maintenance** tab
4. Click **Self-Test** button
5. Select print destination and click **OK**
6. Printer outputs test page; review for quality issues

### Method 3: Network Self-Test (Ethernet Models Only)

1. Open browser and navigate to printer's IP address: `http://<printer-ip>/`
2. Go to **Status** → **Print Test Page**
3. Printer outputs network connectivity and performance report

---

## Maintenance & Supplies

| Item                              | Part Number    | Supplier           | Frequency                       |
| --------------------------------- | -------------- | ------------------ | ------------------------------- |
| **80mm Thermal Paper (BPA-free)** | TM-T88-80BF    | Epson/Local vendor | As needed                       |
| **Cleaning Kit**                  | TM-T88-CLEAN   | Epson              | Quarterly                       |
| **Ink roller (if needed)**        | Not applicable | N/A                | Thermal printers require no ink |
| **AC Power Adapter**              | M303H (24V 5A) | Epson              | On failure                      |

---

## Troubleshooting Quick Reference

| Issue                              | Likely Cause                | First Steps                                             |
| ---------------------------------- | --------------------------- | ------------------------------------------------------- |
| Printer not responding             | USB/Network disconnected    | Check cable connections; restart printer                |
| Print quality poor (faded/streaks) | Thermal head dirty          | Use cleaning kit; perform self-test                     |
| Frequent paper jams                | Low-quality paper used      | Verify 80mm BPA-free thermal paper; inspect rollers     |
| Slow printing                      | Driver issue or spooler jam | Restart print spooler service; reinstall driver v2.12.7 |
| Cannot print over network          | IP configuration incorrect  | Access web interface; verify DHCP/static IP             |
| Error E-5 (overheating)            | Heavy print volume          | Allow 15min cooldown; reduce sustained print jobs       |

---

## Support & Escalation

| Contact                    | Details                                           | Response Time               |
| -------------------------- | ------------------------------------------------- | --------------------------- |
| **Internal L2 Support**    | it-l2@servewell.in                                | 2 hours (business hours)    |
| **IT Help Desk**           | it-support@servewell.in or ext. 4500              | 30 minutes (business hours) |
| **Vendor Support (Epson)** | Phone: +91-124-4183500 / support@epsonindia.co.in | 4-6 hours                   |
| **On-Site Technician**     | Contact IT-L2 for escalation (hardware failures)  | Next business day           |

### Escalation Criteria for L1 → L2

- Multiple error codes persist after self-test
- Hardware component failure (cutter, thermal head)
- Firmware corruption (E-6) or memory errors
- Network connectivity issues affecting multiple printers
- Driver compatibility issues with POS system

---

## Document Information

| Field                | Details                             |
| -------------------- | ----------------------------------- |
| **Document Version** | 1.2                                 |
| **Last Updated**     | 2025-01-15                          |
| **Next Review Date** | 2025-04-15                          |
| **Owner**            | IT Operations — Hospitality Systems |
| **Classification**   | Internal — L1 Support Use           |

---

## Revision History

| Version | Date       | Author | Notes                                                                       |
| ------- | ---------- | ------ | --------------------------------------------------------------------------- |
| 1.0     | 2024-11-10 | IT Ops | Initial specification sheet                                                 |
| 1.1     | 2025-01-01 | IT Ops | Added network configuration section; updated driver versions                |
| 1.2     | 2025-01-15 | IT Ops | Expanded troubleshooting; corrected Ethernet specs; added maintenance table |

---

**For updates or clarifications, contact IT-L2 or the Knowledge Base team.**
