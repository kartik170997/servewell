# NetLink NL-3000 Router — Specification Sheet

## Overview

The NetLink NL-3000 is a dual-band wireless router deployed across ServeWell hospitality properties to provide reliable network connectivity for guest Wi-Fi, operational systems, and property management infrastructure. This device serves as the primary access point for both front-of-house guest networks and back-of-house operational systems.

**Supported Versions:** v2.1, v2.2  
**Target Audience:** L1 and L2 Support Agents

---

## Hardware Specifications

| Specification             | Detail                                 |
| ------------------------- | -------------------------------------- |
| **Model**                 | NetLink NL-3000 v2.1 / v2.2            |
| **Processor**             | Dual-core ARM @ 880 MHz                |
| **RAM**                   | 256 MB DDR3                            |
| **Storage**               | 16 MB Flash Memory                     |
| **Wireless Standard**     | 802.11ac (Wi-Fi 5) / 802.11n (Wi-Fi 4) |
| **Frequency Bands**       | 2.4 GHz (1x1 MIMO), 5 GHz (2x2 MIMO)   |
| **Maximum Throughput**    | Up to 1200 Mbps (combined)             |
| **Ethernet Ports**        | 4x Gigabit LAN + 1x Gigabit WAN        |
| **Power Input**           | 12V / 1.5A DC (external adapter)       |
| **Dimensions**            | 240 × 160 × 35 mm                      |
| **Operating Temperature** | 0–40°C                                 |
| **Humidity Range**        | 10–90% (non-condensing)                |

---

## Software & Firmware

| Component                     | Details                                                           |
| ----------------------------- | ----------------------------------------------------------------- |
| **Operating System**          | Embedded Linux (proprietary NetLink OS)                           |
| **Current Firmware Versions** | v2.1 (Legacy), v2.2 (Current)                                     |
| **Web UI Framework**          | HTTP/HTTPS (port 80/443)                                          |
| **Update Method**             | Manual via Admin UI or automated via ServeWell IT                 |
| **Update Policy**             | Security patches applied quarterly; feature updates semi-annually |
| **End of Support**            | v2.1: 31-Dec-2025; v2.2: 31-Dec-2027                              |

---

## Configuration

### Admin UI Access

- **Default Gateway IP:** `192.168.1.1`
- **Access Protocol:** HTTPS (HTTP redirects to HTTPS)
- **Default Port:** 443
- **Backup HTTP Port:** 8080

### Default Credentials Policy

⚠️ **CRITICAL:** Default credentials must be changed immediately upon deployment.

| Field                | Default Value | Policy                                                |
| -------------------- | ------------- | ----------------------------------------------------- |
| **Username**         | admin         | Must be changed at setup                              |
| **Password**         | NetLink@123   | Must be changed at setup                              |
| **Recovery Account** | support       | Use only for account lockout (requires L2 escalation) |

**Password Requirements:**

- Minimum 12 characters
- Must include: uppercase, lowercase, numbers, special characters (!@#$%^&\*)
- Cannot contain device hostname or "ServeWell"
- Expiration: 90 days (configurable)

### SSID Naming Convention

| Network Type    | SSID Format       | Frequency       | Security                      | Max Clients |
| --------------- | ----------------- | --------------- | ----------------------------- | ----------- |
| **Operational** | `ServeWell-Ops`   | 5 GHz preferred | WPA3 / WPA2                   | 50          |
| **Guest**       | `ServeWell-Guest` | 2.4 GHz / 5 GHz | WPA2 (Open for compatibility) | 100         |
| **Management**  | `ServeWell-Admin` | 5 GHz           | WPA3                          | 20          |

**SSID Broadcast:** Guest network must broadcast SSID; operational networks should have broadcast enabled for device discovery.

### VPN Configuration

| Parameter                  | Specification                            |
| -------------------------- | ---------------------------------------- |
| **VPN Type**               | OpenVPN (primary), IPSec (secondary)     |
| **OpenVPN Port**           | 1194 (UDP preferred, TCP 443 failover)   |
| **IPSec Protocol**         | IKEv2 + AES-256-GCM                      |
| **Certificate Authority**  | ServeWell Internal CA (updated annually) |
| **Certificate Location**   | `/etc/netlink/certs/`                    |
| **VPN Auto-Connect**       | Enabled on router boot                   |
| **VPN Reconnection Retry** | 30 seconds (max 5 retries before alert)  |
| **Data Encryption**        | AES-256-CBC for all VPN traffic          |

**VPN Configuration File Location:** `/etc/netlink/vpn/config.conf`

### DHCP Configuration

| Parameter             | Operational   | Guest         |
| --------------------- | ------------- | ------------- |
| **Pool Start**        | 192.168.1.100 | 192.168.2.100 |
| **Pool End**          | 192.168.1.200 | 192.168.2.200 |
| **Pool Size**         | 101 addresses | 101 addresses |
| **Lease Duration**    | 24 hours      | 4 hours       |
| **Renewal Threshold** | 50%           | 50%           |
| **DNS Primary**       | 8.8.8.8       | 8.8.8.8       |
| **DNS Secondary**     | 8.8.4.4       | 8.8.4.4       |
| **Gateway**           | 192.168.1.1   | 192.168.2.1   |

**Recommended Pool Size:** Minimum 100 addresses per SSID for properties with 50+ devices.

---

## LED Status Indicators

| LED          | Color | State    | Meaning                                 |
| ------------ | ----- | -------- | --------------------------------------- |
| **Power**    | Green | Solid    | Device powered and operational          |
| **Power**    | Amber | Blinking | Boot sequence in progress               |
| **Power**    | Red   | Solid    | Power failure or critical error         |
| **Power**    | Off   | Off      | No power supply                         |
| **Internet** | Green | Solid    | WAN connection established              |
| **Internet** | Amber | Blinking | WAN negotiating connection              |
| **Internet** | Red   | Solid    | WAN disconnected or failover active     |
| **2.4 GHz**  | Green | Blinking | 2.4 GHz radio active, data transmitting |
| **2.4 GHz**  | Amber | Solid    | 2.4 GHz radio enabled but idle          |
| **2.4 GHz**  | Off   | Off      | 2.4 GHz radio disabled                  |
| **5 GHz**    | Green | Blinking | 5 GHz radio active, data transmitting   |
| **5 GHz**    | Amber | Solid    | 5 GHz radio enabled but idle            |
| **5 GHz**    | Off   | Off      | 5 GHz radio disabled                    |

---

## Common Error Codes & Troubleshooting

| Code     | LED Pattern                     | Meaning                   | Immediate Action                                     |
| -------- | ------------------------------- | ------------------------- | ---------------------------------------------------- |
| **E001** | Power: Red (solid)              | Power supply disconnected | Check power adapter; reseat connector                |
| **E002** | Internet: Red (solid) x 5 sec   | WAN cable disconnected    | Verify Ethernet cable in WAN port                    |
| **E003** | Internet: Red (blinking)        | DHCP acquisition timeout  | Power cycle router; check ISP connection             |
| **E004** | All: Blinking red               | Firmware corrupted        | Perform factory reset and reflash firmware           |
| **E005** | 2.4 GHz: Red (solid)            | Radio module failure      | Escalate to L2; may require hardware replacement     |
| **E006** | 5 GHz: Red (solid)              | Radio module failure      | Escalate to L2; may require hardware replacement     |
| **E010** | Internet: Amber (fast blinking) | VPN connection failed     | Check VPN certificate validity; restart VPN service  |
| **E011** | All LEDs: Amber (4 Hz)          | Memory threshold exceeded | Reboot router; if persists, escalate to L2           |
| **E012** | Power: Amber (2 Hz pulse)       | Temperature warning       | Ensure adequate ventilation; check ambient temp      |
| **E099** | Random LED flashing             | Unknown critical error    | Perform factory reset; if issue persists, RMA device |

---

## Factory Reset Procedure

⚠️ **WARNING:** Factory reset erases all custom configurations. Use only as last resort.

### Hardware Reset

1. Ensure device is powered on
2. Locate **RESET** button (recessed, on rear panel)
3. Press and hold reset button for **15 seconds** using a paperclip or stylus
4. Release when all LEDs turn off
5. Device will reboot automatically (2–3 minutes)
6. Wait for **Power LED to turn solid green** and **Internet LED to stabilize**

### Verification

- All SSIDs revert to factory defaults (NetLink-2.4 / NetLink-5)
- Admin credentials reset to `admin` / `NetLink@123`
- All custom VPN and DHCP configurations are removed
- Device will attempt to auto-provision via ServeWell management portal

### Post-Reset Reconfiguration

1. Access Admin UI: `https://192.168.1.1`
2. Login with default credentials
3. Change admin password immediately
4. Re-apply operational SSIDs and security settings
5. Re-configure VPN (if not auto-provisioned)
6. Verify DHCP pools and DNS settings

---

## Web UI Features & Access

| Feature             | Default Port | Notes                                   |
| ------------------- | ------------ | --------------------------------------- |
| **Admin Dashboard** | 443 (HTTPS)  | Full router configuration               |
| **Guest Portal**    | 80 (HTTP)    | Captive portal for guest authentication |
| **Management API**  | 8443 (HTTPS) | ServeWell IT integration endpoint       |
| **Backup/Restore**  | 443 (HTTPS)  | Configuration export/import             |
| **Firmware Update** | 443 (HTTPS)  | Accessible via Admin Dashboard only     |

**Admin UI Login Attempts:** 5 failed attempts = 15-minute lockout

---

## Network Architecture

```
WAN (Internet)
    ↓
[NL-3000 Router]
    ├─ ServeWell-Ops (5 GHz) → Property Operations & PMS
    ├─ ServeWell-Guest (2.4/5 GHz) → Guest Wi-Fi
    └─ ServeWell-Admin (5 GHz) → IT Management

Wired LAN (4x Gigabit)
    ├─ Property Management System
    ├─ Point of Sale
    ├─ Access Control
    └─ Security Systems
```

---

## Performance & Specifications

| Metric                      | Value                                               |
| --------------------------- | --------------------------------------------------- |
| **Max Concurrent Clients**  | 150+ (recommendation: <100 for optimal performance) |
| **Throughput (Real-world)** | 400–600 Mbps (varies by conditions)                 |
| **Latency (LAN)**           | <1 ms                                               |
| **Latency (WAN via VPN)**   | 20–50 ms                                            |
| **Wi-Fi Range**             | 30–50 meters (indoor, line-of-sight)                |
| **Max Transmission Power**  | 20 dBm (FCC compliant)                              |

---

## Support & Escalation

| Contact                  | Email                        | Phone           | Hours           | Escalation                                |
| ------------------------ | ---------------------------- | --------------- | --------------- | ----------------------------------------- |
| **L1 Support**           | support@servewell.in         | 1-800-SERVEWELL | 24/7            | Issues unable to resolve via this guide   |
| **L2 Support**           | it-l2@servewell.in           | Ext. 5500       | 08:00–22:00 IST | Hardware failures, advanced config issues |
| **NetLink Vendor**       | support@netlink-networks.com | +1-408-555-0199 | 09:00–18:00 PST | RMA, hardware defects, firmware bugs      |
| **Emergency (Critical)** | emergency@servewell.in       | 1-800-EMERGENCY | 24/7            | Complete network outage, security breach  |

**SLA Response Times:**

- L1: 15 minutes
- L2: 30 minutes (critical), 2 hours (standard)
- Vendor: 4 hours (critical)

---

## Revision History

| Version | Date       | Author                 | Notes                                                                   |
| ------- | ---------- | ---------------------- | ----------------------------------------------------------------------- |
| 1.0     | 2024-11-01 | IT Infrastructure Team | Initial specification for v2.1 and v2.2                                 |
| 1.1     | 2025-01-15 | IT Infrastructure Team | Added VPN auto-reconnection parameters; updated EOS dates               |
| 1.2     | 2025-02-20 | IT Infrastructure Team | Clarified DHCP pool recommendations; added network architecture diagram |
| 1.3     | 2025-03-10 | IT Infrastructure Team | Updated vendor contact information; added SLA response times            |

---

## Related Documentation

- **NetLink NL-3000 Deployment Guide** — Property setup and installation procedures
- **ServeWell VPN Configuration Guide** — VPN certificate and tunnel setup
- **Guest Wi-Fi Captive Portal Setup** — Guest authentication and acceptance policy
- **Network Security Policy** — SSID encryption and access control standards
- **Troubleshooting Flowchart** — Decision tree for L1 diagnostic support

---

**Document Classification:** Internal Use Only  
**Last Updated:** 10-Mar-2025  
**Next Review Date:** 10-Jun-2025
