# CreamTech Soft Serve Machines — Specification Sheet

## Overview

CreamTech soft serve machines are critical point-of-sale dispensing systems deployed across ServeWell hospitality locations. These units automate soft serve ice cream production and dispensing, requiring reliable operation during high-volume service periods. This specification covers two primary models currently in production deployment, detailing hardware, software, maintenance schedules, and troubleshooting procedures for L1 support agents and field service technicians.

---

## Hardware Specifications

### CreamTech SC-300 v3.1

| Specification        | Details                                  |
| -------------------- | ---------------------------------------- |
| **Processor**        | ARM Cortex-A9 @ 1.2 GHz                  |
| **RAM**              | 512 MB DDR3                              |
| **Storage**          | 4 GB eMMC flash                          |
| **Display**          | 7" capacitive touchscreen (800×480)      |
| **Connectivity**     | Ethernet (RJ-45), Wi-Fi 802.11n optional |
| **Power Input**      | 220-240V AC, 50/60 Hz, 15A               |
| **Compressor**       | Hermetic rotary, 3/4 HP                  |
| **Cooling Capacity** | 200-250 L/hour                           |
| **Dimensions**       | 65 cm (W) × 80 cm (H) × 60 cm (D)        |
| **Weight**           | 95 kg                                    |

### CreamTech SC-500 v2.4

| Specification        | Details                                                |
| -------------------- | ------------------------------------------------------ |
| **Processor**        | ARM Cortex-A53 @ 1.5 GHz (dual-core)                   |
| **RAM**              | 1 GB DDR4                                              |
| **Storage**          | 8 GB eMMC flash                                        |
| **Display**          | 10" capacitive touchscreen (1024×768)                  |
| **Connectivity**     | Dual Ethernet (RJ-45), Wi-Fi 802.11ac, 4G LTE optional |
| **Power Input**      | 220-240V AC, 50/60 Hz, 20A                             |
| **Compressor**       | Hermetic rotary, 1 HP                                  |
| **Cooling Capacity** | 300-350 L/hour                                         |
| **Dimensions**       | 75 cm (W) × 95 cm (H) × 65 cm (D)                      |
| **Weight**           | 125 kg                                                 |

### Key Differences

- **SC-500 v2.4** provides 40% higher cooling capacity, dual-core processing, and enhanced connectivity (LTE support)
- **SC-300 v3.1** is suitable for low-to-medium volume locations; **SC-500 v2.4** recommended for high-traffic venues
- Memory and storage doubled in SC-500 for improved multitasking and data logging

---

## Software & Firmware

| Component                | SC-300 v3.1                                         | SC-500 v2.4                                         |
| ------------------------ | --------------------------------------------------- | --------------------------------------------------- |
| **Base OS**              | Linux 4.14 LTS                                      | Linux 5.4 LTS                                       |
| **Application**          | CreamTech Manager v2.1.3                            | CreamTech Manager v3.2.1                            |
| **Current Firmware**     | 3.1.4 (released 2024-12-15)                         | 2.4.6 (released 2024-11-20)                         |
| **Update Policy**        | Quarterly patches; critical updates within 48 hours | Quarterly patches; critical updates within 48 hours |
| **Last Security Update** | 2025-01-10                                          | 2025-01-08                                          |

### Update Procedure

1. Connect machine to stable network (Ethernet preferred)
2. Navigate to **Settings > System > Firmware Updates**
3. Select **Check for Updates**; approve and confirm
4. Update typically completes in 8-12 minutes; machine enters service mode (unavailable for sales)
5. Verify successful boot and operational status post-update

---

## Configuration

### Default Operating Parameters

| Parameter                 | SC-300 v3.1         | SC-500 v2.4         | Notes                                           |
| ------------------------- | ------------------- | ------------------- | ----------------------------------------------- |
| **Ambient Temp. Range**   | 15-32°C             | 15-35°C             | See E04 issue below                             |
| **Operating Temp. Range** | 4-6°C (mix chamber) | 4-6°C (mix chamber) | Critical for product quality                    |
| **Humidity Range**        | 30-80% RH           | 30-80% RH           | High humidity may trigger condensation warnings |
| **Voltage Tolerance**     | ±10% (198-264V)     | ±10% (198-264V)     | Unstable supply triggers E11                    |

### Configuration File Locations

- **Main Config** `/etc/creamtech/config.json`
- **Temperature Logs** `/var/log/creamtech/thermal.log`
- **Event Logs** `/var/log/creamtech/events.log`
- **Network Config** `/etc/network/interfaces`

### Key Configuration Parameters

```
{
  "mix_target_temp": 5,
  "compressor_max_runtime": 1800,
  "cleaning_interval_hours": 24,
  "error_log_retention_days": 90,
  "ntp_server": "ntp.servewell.in",
  "reporting_interval_minutes": 15
}
```

---

## Cleaning & Maintenance Schedule

### Daily Cleaning Cycle

| Task                | Frequency                 | Duration  | Instructions                                                  |
| ------------------- | ------------------------- | --------- | ------------------------------------------------------------- |
| **Rinse Cycle**     | End of service            | 8 minutes | Navigate to **Maintenance > Rinse**; dispense mix until clear |
| **Nozzle Purge**    | After each shift          | 2 minutes | Press **Purge** button on control panel                       |
| **Drip Tray Empty** | As needed (min. 2x daily) | 5 minutes | Remove and rinse drip tray; empty condensation reservoir      |

### Weekly Cleaning

- **Hopper inspection**: Check for residue or ice crystals
- **Filter replacement** (if applicable): Cartridge filters every 2 weeks or per pressure indicator
- **Compressor coil cleaning**: Gently vacuum external condenser coils

### Monthly Deep Clean (Requires Service Technician)

- Disassemble mix chamber for thorough cleaning
- Inspect refrigerant lines for leaks (use UV tracer dye)
- Test all temperature sensors with calibration device
- Lubricate compressor bearings (per CreamTech maintenance manual)
- Verify electrical connections; document resistance readings

### Annual Service

- **Compressor overhaul or replacement** (check compressor hours via log)
- **Refrigerant analysis and potential recharge**
- **Complete electrical system inspection**
- **Firmware upgrade and backup configuration**

---

## Error Codes & Indicators

### Error Code Reference Table (E01–E12)

| Code    | Description                      | Severity | Cause(s)                                                                          | Resolution                                                                                                                 |
| ------- | -------------------------------- | -------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **E01** | Compressor overheat              | Critical | Condenser coils clogged; ambient >35°C; refrigerant leak                          | Power off immediately. Inspect condenser; vacuum coils. Check ambient temp. Contact L2 if persists.                        |
| **E02** | Temperature sensor failure       | High     | Faulty RTD sensor; loose wiring; corroded connector                               | Restart machine. If error persists, replace sensor (part #CS-TEMP-01). Verify connector seating.                           |
| **E03** | Low refrigerant pressure         | High     | Refrigerant leak; compressor inefficiency; blocked capillary tube                 | Do not attempt repair. Schedule L2/vendor service. Document pressure reading if available.                                 |
| **E04** | Ambient temperature out of range | Medium   | Ambient >32°C (SC-300) or >35°C (SC-500); inadequate ventilation                  | Improve venue ventilation. Move machine away from heat source. See **Known Issues** section.                               |
| **E05** | Electrical supply voltage low    | High     | Unstable grid power; undersized electrical circuit; tripped breaker               | Check facility breaker/panel. Verify 220-240V ±10%. Contact facility management. Do not override.                          |
| **E06** | Network connectivity lost        | Low      | Ethernet/Wi-Fi disconnection; router down; DNS failure                            | Check network cable seating. Restart router. Verify IP configuration via **Settings > Network**. Reboot machine if needed. |
| **E07** | Memory usage critical            | Medium   | Corrupted log files; insufficient storage space; system hang                      | Clear event logs: **Settings > System > Maintenance > Clear Logs**. Perform soft restart if unresponsive.                  |
| **E08** | Pump/motor malfunction           | Critical | Pump bearing failure; cavitation; electrical issue; blocked discharge             | Power off. Check for clogs or debris in discharge line. Do not attempt motor repair; escalate to L2/vendor.                |
| **E09** | Hopper level sensor error        | Low      | Sensor misalignment; broken sensor; loose wiring                                  | Inspect sensor lens for dirt; clean with lint-free cloth. Verify mechanical hopper position. Reseat connector.             |
| **E10** | Compressor safety lockout        | Critical | Multiple thermal events; persistent overheat condition; system shutdown triggered | Machine will not restart for 30 minutes. Investigate root cause (ambient, condenser, airflow). Contact L2 if repeated.     |
| **E11** | Power supply unit failure        | Critical | Failed PSU capacitor; input voltage instability; internal short                   | Do not attempt repair. Escalate to L2 for PSU replacement. Verify facility power quality.                                  |
| **E12** | Firmware checksum error          | High     | Corrupted firmware; interrupted update; flash memory fault                        | Attempt firmware re-flash from **Settings > System > Firmware Updates > Restore**. If fails, contact vendor support.       |

---

## Known Issues & Resolutions

### SC-300 v3.1 — Ambient Heat Issue (E04 Frequent Triggering)

**Affected Units:** SC-300 v3.1 serial numbers SC300-2023-00001 through SC300-2024-06999

**Issue Description:**
Units deployed in high-ambient environments (venues with poor AC, direct sunlight, or kitchen proximity) frequently trigger E04 errors even when ambient is within specification (15-32°C). Root cause: undersized condenser in early v3.1 batches insufficient for ambient edge cases.

**Impact:**

- Machine enters protective shutdown; 30-minute restart lockout
- Service disruption during peak hours
- Repeated thermal cycling degrades compressor lifespan

**Permanent Fix — Firmware Patch v3.1.5:**
Released January 2025; implements adaptive temperature thresholds:

- Raises ambient upper threshold to 35°C (matching SC-500 tolerance)
- Introduces dynamic compressor duty-cycle throttling at 30-32°C to prevent overshoot
- Improves sensor averaging algorithm to reduce false positives

**Installation Instructions:**

1. Connect SC-300 v3.1 unit to Ethernet
2. Navigate to **Settings > System > Firmware Updates**
3. Select **Check for Updates**; v3.1.5 will be available
4. Approve update and allow 10-minute cycle
5. **Highly recommended:** After update, verify ambient sensor calibration (**Settings > Diagnostics > Sensor Test**)

**Temporary Workaround (Pre-Update):**

- Improve venue ventilation: ensure minimum 1 meter clearance from heat sources
- Schedule operation outside peak ambient heat hours if possible
- Reduce compressor duty by limiting simultaneous dispenses; allow cool-down between cycles

**Additional Resources:**

- CreamTech Technical Bulletin TB-2025-E04
- Venue Site Survey Guide (HVAC adequacy checklist)

---

## Support & Escalation

### Internal Support Contacts

| Tier   | Team                | Contact                                 | Hours                 | Scope                                                                          |
| ------ | ------------------- | --------------------------------------- | --------------------- | ------------------------------------------------------------------------------ |
| **L1** | On-site Support     | Your line manager / ServeWell Help Desk | 06:00–22:00 IST       | Password resets, basic connectivity, error code lookup, cleaning guidance      |
| **L2** | IT Infrastructure   | it-l2@servewell.in                      | 08:00–18:00 IST (M–F) | Hardware replacement, firmware updates, network diagnostics, persistent errors |
| **L3** | Systems Engineering | it-l3@servewell.in                      | 08:00–18:00 IST (M–F) | Architecture changes, multi-unit issues, vendor escalations                    |

### Vendor Support (CreamTech Direct)

| Contact Type             | Details                                                      |
| ------------------------ | ------------------------------------------------------------ |
| **Support Portal**       | https://support.creamtech.com (login via ServeWell account)  |
| **Phone (India)**        | +91-11-XXXX-XXXX (available 09:00–18:00 IST, Mon–Fri)        |
| **Email (Tier 1)**       | support@creamtech.com                                        |
| **Email (Critical)**     | critical-support@creamtech.com (for E01, E10, E11, E12 only) |
| **Service Request Form** | https://support.creamtech.com/tickets/new                    |
| **Spare Parts**          | parts@creamtech.com                                          |

### Escalation Path

1. **L1 agent** → Attempt resolution using this spec sheet and error code table
2. **If unresolved after 30 min.** → Contact L2 (it-l2@servewell.in) with:
   - Machine model and serial number
   - Error code and timestamp
   - Steps already attempted
   - Venue ambient conditions
3. **If hardware failure suspected** → L2 files vendor ticket with CreamTech critical support
4. **Spare parts & on-site service** → Coordinated by L2; typical lead time 2–3 business days

---

## Revision History

| Version | Date       | Author      | Notes                                                                                                               |
| ------- | ---------- | ----------- | ------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2024-10-15 | IT Ops Team | Initial specification for SC-300 v3.1 and SC-500 v2.4                                                               |
| 1.1     | 2025-01-10 | IT Ops Team | Added E04 ambient heat issue, firmware patch v3.1.5, expanded error code table, corrected SC-500 connectivity specs |
| 1.2     | 2025-02-01 | IT Ops Team | Updated support contact hours; added venue site survey link; clarified monthly service intervals                    |

---

## Document Control

**Classification:** Internal – ServeWell Hospitality  
**Last Updated:** February 1, 2025  
**Next Review Date:** May 1, 2025  
**Owner:** IT Infrastructure Team (it-l2@servewell.in)

For questions or corrections, contact the IT Infrastructure team.
