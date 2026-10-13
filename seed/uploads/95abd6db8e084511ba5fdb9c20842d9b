# FrostyPro 800 Soft Serve Machine — Specification Sheet

## Overview

The FrostyPro 800 is a commercial soft serve ice cream machine designed for high-volume hospitality environments. It serves as a critical revenue-generating point-of-sale asset across ServeWell's managed locations, providing consistent product quality and operational reliability. This specification sheet covers firmware versions v1.8 and v2.0 and is intended to support L1 troubleshooting and field service operations.

---

## Hardware Specifications

| Component                 | Specification                              |
| ------------------------- | ------------------------------------------ |
| **Processor**             | ARM Cortex-A9 @ 1.2 GHz                    |
| **RAM**                   | 512 MB DDR3                                |
| **Storage**               | 2 GB eMMC Flash                            |
| **Display**               | 7" capacitive touchscreen (800×480)        |
| **Network Interface**     | Ethernet (RJ-45) + optional 4G/WiFi module |
| **Power Requirements**    | 220–240V AC, 50/60 Hz, 16A circuit         |
| **Operating Temperature** | 5–35°C ambient                             |
| **Dimensions**            | 560 × 680 × 1,420 mm (W × D × H)           |
| **Weight**                | 85 kg                                      |

---

## Software & Firmware

| Item                     | Details                                                        |
| ------------------------ | -------------------------------------------------------------- |
| **Operating System**     | Linux-based (Custom kernel v4.9+)                              |
| **Application Versions** | v1.8, v2.0 (LTS)                                               |
| **Current Recommended**  | v2.0 (v1.8 in maintenance mode)                                |
| **Update Policy**        | Over-the-air (OTA) updates monthly; critical patches as needed |
| **Update Method**        | WiFi/Ethernet via ServeWell Management Portal                  |
| **Downtime (typical)**   | 5–10 minutes per update                                        |

---

## Configuration

### Key Operating Parameters

| Parameter                          | Default | Min | Max | Unit    |
| ---------------------------------- | ------- | --- | --- | ------- |
| **Mix Level Threshold (Optimal)**  | 75–85   | 60  | 100 | %       |
| **Mix Level Threshold (Low)**      | < 30    | —   | —   | %       |
| **Mix Level Threshold (Critical)** | < 10    | —   | —   | %       |
| **Dispensing Temperature**         | 4–6     | 2   | 8   | °C      |
| **Cycle Time (per serve)**         | 8–12    | —   | —   | seconds |
| **Auto-Shutoff (idle)**            | 120     | 60  | 300 | minutes |

### Configuration File Locations

- **Primary Config:** `/etc/frostypro/device.conf`
- **Mix Level Config:** `/etc/frostypro/mix_thresholds.conf`
- **Log Directory:** `/var/log/frostypro/`
- **Firmware Binary:** `/opt/frostypro/firmware.bin`

### Default Settings (Factory Reset)

- Mix Level Warnings: **Enabled**
- Temperature Monitoring: **Enabled**
- Remote Diagnostics: **Enabled**
- Automatic Shutdown on Critical Error: **Enabled**

---

## Error Codes & Indicators

### Error Code Reference Table (F01–F08)

| Code    | Severity    | Description                          | L1 Action                                                              | L2 Escalation                              |
| ------- | ----------- | ------------------------------------ | ---------------------------------------------------------------------- | ------------------------------------------ |
| **F01** | ⚠️ Warning  | Mix level low (30–50%)               | Refill mix reservoir; check pour pattern                               | If recurring within 2 hrs                  |
| **F02** | 🔴 Critical | Mix level critical (< 10%)           | **STOP operations.** Refill immediately. See Known Issues (v1.8).      | Immediate if v1.8 detected                 |
| **F03** | ⚠️ Warning  | Temperature sensor fault             | Power cycle machine; verify sensor cable connection                    | If fault persists after restart            |
| **F04** | 🔴 Critical | Compressor malfunction               | Power off; wait 5 min; restart. Check compressor noise.                | If compressor unresponsive                 |
| **F05** | ⚠️ Warning  | Touchscreen unresponsive             | Restart machine; tap calibration prompt if shown                       | If unresponsive after 2 restarts           |
| **F06** | 🔴 Critical | Network connectivity lost            | Verify Ethernet cable / WiFi signal; restart network module            | If offline > 30 minutes                    |
| **F07** | ⚠️ Warning  | Firmware update available            | Notify venue manager; schedule update outside peak hours               | N/A (informational)                        |
| **F08** | 🔴 Critical | Internal system error / kernel panic | Force restart (hold power 10 sec); check logs in `/var/log/frostypro/` | Provide error logs; assess hardware damage |

---

## Known Issues & Workarounds

### FrostyPro 800 v1.8 — Mix Overrun Issue

**Affected Versions:** v1.8 only  
**Severity:** Medium  
**Description:** When mix level falls below 10%, the machine's low-level sensor may fail to halt dispensing, resulting in continued operation beyond critical threshold. This can damage the pump assembly.

**Symptoms:**

- F02 error triggered but dispensing continues
- Mix reservoir drains completely
- Unusual grinding/rattling noise from pump

**Resolution:**

1. **Immediate:** Power off the machine immediately
2. **Manual Override:** Follow Section 5.3 procedure to stop dispensing
3. **Refill:** Top up mix to ≥ 60% before resuming operation
4. **Upgrade:** **Strongly recommend upgrading to v2.0** (fix confirmed in release notes)
5. **Escalate:** Report incident to L2 with timestamps and error logs

---

## Manual Override Procedure (Section 5.3)

Use this procedure only for emergency situations (e.g., F02 triggered but dispensing unresponsive, or critical errors during operation).

### Emergency Stop

1. **Press and hold the red power button** (bottom right of machine, 5 seconds minimum) until the display goes black
2. **Wait 10 seconds** for capacitors to discharge
3. **Flip the circuit breaker** to OFF (if accessible; typically located behind or underneath machine)
4. **Wait 30 seconds**

### Manual Pump Shutoff

5. Locate the **manual shut-off valve** on the mix supply line (chrome lever, typically left rear of machine)
6. **Rotate the lever 90° clockwise** to the CLOSED position (lever should be perpendicular to tube)
7. Verify no dispensing occurs when power is restored

### Resuming Normal Operation

8. Rotate the shut-off valve **90° counter-clockwise** back to OPEN
9. Restore power via circuit breaker
10. **Wait 2 minutes** for system initialization and self-diagnostics
11. Press the green power button to restart the display
12. Verify F02 error is cleared before resuming service
13. **Do not proceed** if error reappears—escalate immediately

**⚠️ Warning:** Manual override should only be performed by trained technicians. Improper closure of the shut-off valve may cause internal pressure buildup.

---

## Support & Escalation

| Contact                      | Role                     | Details                                                                                                         | Availability                               |
| ---------------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| **L1 Support (On-Site)**     | First response           | Venue manager or on-site technician                                                                             | During business hours                      |
| **L2 Support**               | Technical escalation     | it-l2@servewell.in                                                                                              | 09:00–18:00 IST, Mon–Fri                   |
| **FrostyPro Vendor Support** | Hardware/firmware vendor | **support@frostypro-global.com** <br> **Phone:** +1-800-FROSTY-1 (US) <br> **Response SLA:** 4 hours (critical) | 24/5 (US hours); escalation queue for APAC |
| **ServeWell Spare Parts**    | Equipment procurement    | parts@servewell.in                                                                                              | Email ticket system                        |

### Escalation Criteria

- **Immediate (to Vendor):** Critical errors (F02, F04, F08) unresolved after manual restart
- **Same-day (to L2):** Recurring warnings (F01, F03) within 24 hours
- **Scheduled:** Feature requests, non-critical updates, routine maintenance

---

## Revision History

| Version | Date       | Author        | Notes                                                                             |
| ------- | ---------- | ------------- | --------------------------------------------------------------------------------- |
| 1.0     | 2025-01-15 | IT Operations | Initial specification; v1.8 & v2.0 support                                        |
| 1.1     | 2025-08-01 | Support Team  | Added v1.8 known overrun issue (Section 3.1); clarified manual override steps     |
| 1.2     | 2025-09-10 | Documentation | Updated vendor contact; added escalation matrix; added mix level thresholds table |

---

## Appendix: Quick Reference Card

**Error F02 (Critical):** Stop. Refill. v1.8? → Upgrade to v2.0  
**Error F04 (Compressor):** Off 5min → Restart → Listen for noise  
**Error F08 (System):** Force restart (hold 10s) → Check logs → Escalate  
**Manual Override:** Red button 5s → Circuit OFF → 30s wait → Close valve  
**Vendor Contact:** support@frostypro-global.com | +1-800-FROSTY-1 (US)

---

**Document Classification:** ServeWell Internal — Restricted to Support & Service Personnel  
**Next Review Date:** 2026-09-10
