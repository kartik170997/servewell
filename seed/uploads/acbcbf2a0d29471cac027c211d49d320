# OrbitPOS — System Specification Sheet

## Overview

OrbitPOS is ServeWell Hospitality's primary point-of-sale system, responsible for transaction processing, order management, and payment authorization across all front-of-house operations. This specification sheet covers versions 2.0 and 2.1 and is intended to support L1 and L2 technical support agents in troubleshooting and escalation workflows.

---

## Hardware Specifications

| Component        | Requirement                                                                             |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Processor**    | Intel Core i5 (6th Gen) or equivalent; minimum 2.0 GHz dual-core                        |
| **RAM**          | 8 GB minimum; 16 GB recommended                                                         |
| **Storage**      | 256 GB SSD (preferred); 128 GB minimum HDD                                              |
| **Display**      | 15–17" touchscreen (capacitive); minimum 1024×768 resolution                            |
| **Connectivity** | Gigabit Ethernet (primary); Wi-Fi 5 (802.11ac) as secondary failover                    |
| **Peripherals**  | Integrated receipt printer, cash drawer (USB/serial), barcode scanner, customer display |
| **Power Supply** | Uninterruptible Power Supply (UPS) recommended; 15-minute minimum runtime               |
| **Network**      | Requires connection to ServeWell central server; latency <100 ms                        |

---

## Software & Firmware

| Item                     | Details                                                                  |
| ------------------------ | ------------------------------------------------------------------------ |
| **Operating System**     | Windows 10 Enterprise (Build 19042+) or Windows Server 2019              |
| **Application Versions** | OrbitPOS v2.0 (Legacy); OrbitPOS v2.1 (Current)                          |
| **Database**             | SQL Server 2016 SP2 or later; local caching with cloud sync              |
| **Update Policy**        | Automatic patches: Monthly (2nd Tuesday); Security hotfixes: As required |
| **Firmware**             | Peripheral drivers updated quarterly; managed via centralized deployment |
| **.NET Framework**       | .NET Framework 4.7.2 (minimum)                                           |

---

## Configuration

### Key Parameters

| Parameter               | Default Value   | Notes                                 |
| ----------------------- | --------------- | ------------------------------------- |
| **Transaction Timeout** | 45 seconds      | Adjustable via admin portal           |
| **Offline Mode**        | Enabled         | Automatic fallback if connection lost |
| **Receipt Format**      | 80 mm thermal   | Configurable per location             |
| **Shift Duration**      | 8 hours         | Modifiable by venue manager           |
| **Sync Interval**       | Every 5 minutes | Cloud sync frequency                  |

### File & Registry Paths

- **Config File:** `C:\ProgramData\OrbitPOS\config.xml`
- **Database Location:** `C:\OrbitPOS\Data\transactions.mdf`
- **Logs Directory:** `C:\OrbitPOS\Logs\` (auto-rotate; 30-day retention)
- **Registry Key:** `HKEY_LOCAL_MACHINE\SOFTWARE\OrbitTech\OrbitPOS`

### Admin Portal Access

- **URL:** `https://admin.orbitpos.servewell.in`
- **Authentication:** Azure AD (ServeWell domain credentials)
- **Port:** 443 (HTTPS only)
- **Typical Uses:** License management, terminal configuration, transaction reports, user permissions

---

## Known Issues & Fixes

### DRAWER_VOID Bug (v2.0)

**Issue:** Cash drawer fails to register void transactions, resulting in incorrect cash reconciliation. Error code: `DRW_ERR_0x2E`.

**Affected Versions:** OrbitPOS v2.0 (all builds prior to 2.0.847)

**Symptoms:**

- Void transactions process but drawer does not open
- Cash audit reports show discrepancies
- Error logged: "DRAWER_VOID exception in transaction handler"

**Resolution:**

1. **Immediate:** Manually reconcile cash drawer at shift end using the "Manual Adjustment" function in Reports menu
2. **Permanent Fix:** Upgrade to OrbitPOS v2.1 (build 2.1.105+), which includes the corrected DRAWER_VOID handler
3. **Upgrade Steps:**
   - Back up current database: `C:\OrbitPOS\Data\transactions.mdf`
   - Download v2.1 installer from admin portal
   - Run installer with admin privileges; restart terminal
   - Validate void transactions post-upgrade

**Reference:** Vendor ticket #ORB-2024-4421

---

## Error Codes & Indicators

| Error Code      | Meaning                        | Severity | Action                                                         |
| --------------- | ------------------------------ | -------- | -------------------------------------------------------------- |
| `DRW_ERR_0x2E`  | Drawer void transaction failed | High     | See DRAWER_VOID bug section; escalate if persists post-upgrade |
| `NET_ERR_0x01`  | Network connection lost        | Medium   | Check Ethernet/Wi-Fi; verify server availability               |
| `DB_ERR_0x15`   | Database sync timeout          | High     | Restart terminal; check SQL Server status                      |
| `AUTH_ERR_0x0A` | User authentication failed     | Low      | Verify credentials; reset password via admin portal            |
| `PMT_ERR_0x3F`  | Payment gateway timeout        | Medium   | Retry transaction; check payment processor status              |
| `HW_ERR_0x08`   | Printer offline                | Low      | Check power/USB connection; reinstall driver                   |
| `MEM_WARN_0x12` | Low memory warning             | Medium   | Close unnecessary applications; restart if critical            |

---

## Support & Escalation

### Internal Support Contacts

| Contact                   | Details                       | Availability             |
| ------------------------- | ----------------------------- | ------------------------ |
| **L1 Help Desk**          | `helpdesk@servewell.in`       | Mon–Fri, 08:00–18:00 IST |
| **L2 Technical Team**     | `it-l2@servewell.in`          | Mon–Fri, 09:00–17:00 IST |
| **After-Hours Emergency** | `+91-22-XXXX-5555` (ext. 999) | 24/7                     |

### Vendor Escalation

| Vendor                                      | Contact Method                                          | Response SLA            |
| ------------------------------------------- | ------------------------------------------------------- | ----------------------- |
| **OrbitTech Systems Ltd** (Primary Support) | `support@orbittech.com`                                 | 4 business hours        |
| **Vendor Phone**                            | `+1-800-ORBITPOS`                                       | 8:00–20:00 EST, Mon–Fri |
| **Vendor Portal**                           | `https://support.orbittech.com` (requires ticket login) | Self-service resources  |

### Escalation Path

1. **L1 Detection:** Agent logs issue in ServiceNow (ticket auto-created)
2. **L1 Troubleshooting:** Basic checks (connectivity, restart, logs review)
3. **L2 Escalation:** Forward ticket if issue unresolved after 30 minutes
4. **Vendor Escalation:** L2 submits ticket to OrbitTech for bugs/firmware issues (reference: ticket #ORB-XXXXX)

---

## Revision History

| Version | Date       | Author           | Notes                                                    |
| ------- | ---------- | ---------------- | -------------------------------------------------------- |
| 1.0     | 2024-12-15 | IT Documentation | Initial release                                          |
| 1.1     | 2025-02-20 | IT Documentation | Added DRAWER_VOID bug & fix; updated v2.1 specs          |
| 1.2     | 2025-08-01 | IT Documentation | Updated vendor contact; added after-hours support number |

---

## Additional Resources

- **Knowledge Base:** [ServeWell Wiki: OrbitPOS Troubleshooting](https://wiki.servewell.in/orbitpos)
- **Video Training:** [L1 Setup & Common Issues](https://training.servewell.in)
- **Quick Reference Card:** [OrbitPOS Error Code Poster](https://wiki.servewell.in/orbitpos/poster)

---

**Document Classification:** Internal Use – L1/L2 Support  
**Last Updated:** August 1, 2025  
**Next Review Date:** February 1, 2026
