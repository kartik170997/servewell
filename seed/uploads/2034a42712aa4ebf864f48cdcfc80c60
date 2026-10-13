# FoodTech POS — System Specification Sheet

## Overview

FoodTech POS v4.2.x and v5.1.x is a mission-critical point-of-sale system deployed across ServeWell Hospitality locations for order processing, payment handling, and inventory management. This specification sheet provides L1 and L2 support agents with technical reference documentation for system deployment, troubleshooting, and maintenance.

**Supported Versions:** v4.2.1, v4.2.2, v4.2.3, v5.1.0, v5.1.1

---

## Hardware Specifications

| Component             | Minimum Requirement                   | Recommended Specification                   |
| --------------------- | ------------------------------------- | ------------------------------------------- |
| **Processor**         | Intel Core i5 (6th Gen) or equivalent | Intel Core i7 (8th Gen) or higher           |
| **RAM**               | 4 GB DDR4                             | 8 GB DDR4                                   |
| **Storage**           | 128 GB SSD                            | 256 GB SSD (7,200 RPM minimum)              |
| **Display**           | 1024×768 @ 60Hz                       | 1920×1080 @ 60Hz                            |
| **Network Interface** | 1 x Gigabit Ethernet                  | 2 x Gigabit Ethernet (primary + failover)   |
| **Peripherals**       | USB 2.0 (4 ports minimum)             | USB 3.0 (6+ ports)                          |
| **Power Supply**      | 300W                                  | 500W UPS-compatible                         |
| **Physical**          | Standard POS terminal form factor     | Wall-mounted or countertop mounting bracket |

---

## Software & Firmware

### Operating System

- **OS:** Windows 10 IoT Enterprise LTSC 2019 or later
- **Build:** Build 17763 or higher
- **.NET Framework:** 4.8 or later
- **Service Packs:** Latest Windows Update patches required

### Application Versions

| Version | Release Date | Status           | EOL Date   |
| ------- | ------------ | ---------------- | ---------- |
| v4.2.1  | 2023-06-15   | Legacy Support   | 2025-12-31 |
| v4.2.2  | 2023-09-20   | Legacy Support   | 2025-12-31 |
| v4.2.3  | 2024-02-10   | Standard Support | 2026-06-30 |
| v5.1.0  | 2024-08-01   | Current          | 2027-12-31 |
| v5.1.1  | 2025-01-15   | Current (Latest) | 2027-12-31 |

### Update Policy

- Critical security patches: Deploy within 48 hours
- Standard updates: Monthly deployment windows (2nd Tuesday)
- Major version upgrades: Scheduled during off-peak hours with 2-week notice

---

## Configuration

### Default Administrator Credentials

⚠️ **IMPORTANT:** Change default credentials immediately after initial deployment.

- **Default Username:** `admin`
- **Default Password:** Located in sealed envelope accompanying hardware shipment (labeled "FoodTech POS Admin Credentials")
- **Credentials Storage Policy:** Store in encrypted password manager; never document in plaintext
- **Password Change:** First login must change default password (enforced by system)
- **Account Lockout:** 5 failed login attempts locks account for 30 minutes

### Critical File Paths

| Path                                      | Purpose                        | Notes                           |
| ----------------------------------------- | ------------------------------ | ------------------------------- |
| `C:\FoodTechPOS\config\`                  | Configuration files (XML)      | Requires backup before edits    |
| `C:\FoodTechPOS\logs\`                    | Application event logs         | Rotated daily; 30-day retention |
| `C:\ProgramData\FoodTechPOS\db\`          | Local SQLite database cache    | ~500MB typical size             |
| `C:\Windows\System32\drivers\etc\hosts`   | Network host bindings          | Required for offline mode       |
| `%APPDATA%\FoodTechPOS\user_settings.ini` | User preferences (per-profile) | Automatically synced            |

### Registry Paths

- **HKLM:** `HKEY_LOCAL_MACHINE\Software\ServeWell\FoodTechPOS\`
- **HKCU:** `HKEY_CURRENT_USER\Software\ServeWell\FoodTechPOS\`

### Key Configuration Parameters

```
[Database]
DatabaseServer = Central-DB-Server.servewell.local
DatabasePort = 5432
SyncInterval = 300 (seconds)
OfflineMode = Enabled

[Network]
PrimaryServer = pos-api.servewell.in:8443
SecondaryServer = pos-api-dr.servewell.in:8443
TimeoutSeconds = 30
RetryAttempts = 3

[Security]
EncryptionMethod = AES-256-GCM
CertificateLocation = C:\FoodTechPOS\certs\
SessionTimeout = 3600 (seconds)

[Payments]
PCI-DSS Compliance = Enabled
TokenizationRequired = True
DisableMagneticStripe = False
```

---

## Network Requirements

### Port Configuration

| Port     | Protocol   | Direction | Purpose                       | Required    |
| -------- | ---------- | --------- | ----------------------------- | ----------- |
| 443      | HTTPS/TLS  | Outbound  | API communication (primary)   | Yes         |
| 8443     | HTTPS/TLS  | Outbound  | API communication (secondary) | Yes         |
| 5432     | PostgreSQL | Outbound  | Database synchronization      | Yes         |
| 53       | DNS        | Outbound  | Domain name resolution        | Yes         |
| 123      | NTP        | Outbound  | Time synchronization          | Yes         |
| 3389     | RDP        | Inbound   | Remote support (L2 only)      | Conditional |
| 139, 445 | SMB        | Inbound   | Shared file access            | Conditional |
| 9100     | RAW Print  | Outbound  | Receipt printer communication | Conditional |

### Network Requirements

- **Bandwidth:** Minimum 5 Mbps download / 2 Mbps upload
- **Latency:** Maximum 100ms round-trip to primary API server
- **Packet Loss:** <0.5%
- **DNS Resolution:** Must resolve servewell.in domain names
- **Firewall:** Whitelist above ports; block all other outbound traffic

---

## Log File Management

### Log Locations & Retention

| Log File        | Path                                     | Rotation             | Retention | Severity Levels                    |
| --------------- | ---------------------------------------- | -------------------- | --------- | ---------------------------------- |
| Application Log | `C:\FoodTechPOS\logs\app_*.log`          | Daily (midnight UTC) | 30 days   | INFO, WARN, ERROR, FATAL           |
| Transaction Log | `C:\FoodTechPOS\logs\transactions_*.log` | Daily                | 90 days   | All transactions (PII redacted)    |
| Sync Log        | `C:\FoodTechPOS\logs\sync_*.log`         | Daily                | 30 days   | INFO, WARN, ERROR                  |
| Security Log    | `C:\FoodTechPOS\logs\security_*.log`     | Weekly               | 1 year    | Login attempts, permission changes |
| System Events   | Windows Event Viewer                     | System-managed       | 30 days   | Windows application logs           |

### Log File Format

```
[YYYY-MM-DD HH:MM:SS.mmm] [LEVEL] [MODULE] Message | Context=value
2025-01-20 14:32:15.642 [ERROR] [OrderProcessor] Failed to sync transaction | OrderID=ORD-987654, ErrorCode=E1004
```

### Accessing Logs

**L1 Support:** Check most recent 5 logs for obvious errors
**L2 Support:** Full log analysis; use Event Viewer and centralized logging via Splunk (`https://splunk.servewell.in`)

---

## Backup & Restore Procedures

### Backup Strategy

#### Automatic Backups

- **Frequency:** Every 4 hours
- **Location:** Network share `\\backup-nas.servewell.local\foodtech-pos\`
- **Retention:** 14-day rolling window
- **Scope:** Database, configuration files, user settings

#### Manual Backup (L2 Procedure)

```powershell
# Run as Administrator
cd C:\FoodTechPOS\bin\
.\BackupUtility.exe -mode=full -destination=\\backup-nas.servewell.local\foodtech-pos\manual\ -compress=true
```

### Restore Procedures

#### Quick Restore (Configuration Only)

**Use Case:** Configuration corruption or accidental setting changes

```powershell
cd C:\FoodTechPOS\bin\
.\RestoreUtility.exe -mode=config -backup-date=YYYY-MM-DD -version=latest
# Restart service after completion
Restart-Service FoodTechPOS
```

#### Full System Restore (Database + Configuration)

**Use Case:** Data corruption, major failure, or security incident

```powershell
# CRITICAL: Requires L2 approval and maintenance window
cd C:\FoodTechPOS\bin\
.\RestoreUtility.exe -mode=full -backup-date=YYYY-MM-DD -verify=true
# System will automatically restart and re-sync with central server
```

**Estimated Restore Times:**

- Configuration-only: 5–10 minutes
- Full system (local DB <1GB): 30–45 minutes
- Full system with network validation: 60–90 minutes

### Backup Verification

- Verify backup integrity weekly (automated, check `C:\FoodTechPOS\logs\backup_verification.log`)
- L2 performs monthly restore drills using non-production backup copy
- Test restore from oldest backup in retention window quarterly

---

## Version Upgrade Path

### Supported Upgrade Paths

```
v4.2.1 → v4.2.2 → v4.2.3 → v5.1.0 → v5.1.1 (Current)
         (direct)   (direct)   (major)  (patch)
```

**Important:** v4.x → v5.x is a major version upgrade requiring full database migration.

### Upgrade Procedure (L2 Only)

#### Step 1: Pre-Upgrade Checklist

- [ ] Full backup completed and verified
- [ ] Confirm network connectivity and API availability
- [ ] Check available storage: ≥500 MB free space required
- [ ] Schedule during off-peak hours (ideally 2–4 AM)
- [ ] Notify location manager; POS will be unavailable for 30–60 minutes

#### Step 2: Stop Services

```powershell
Stop-Service FoodTechPOS -Force
Stop-Service FoodTechPOS-Sync -Force
```

#### Step 3: Run Upgrade

```powershell
cd C:\FoodTechPOS\upgrades\
.\FoodTechPOS_Upgrade_v5.1.1.exe -source=v5.1.0 -destination=C:\FoodTechPOS\ -autoconfig=true
```

#### Step 4: Post-Upgrade Validation

```powershell
# Verify version
cd C:\FoodTechPOS\bin\
.\FoodTechPOS.exe --version

# Check connectivity
.\DiagnosticTool.exe -test=api-connectivity -test=database-sync -test=services

# Review upgrade log
type C:\FoodTechPOS\logs\upgrade_*.log | Select-String -Pattern "ERROR|FATAL"
```

#### Step 5: Start Services & Monitor

```powershell
Start-Service FoodTechPOS
Start-Service FoodTechPOS-Sync
# Monitor logs for 30 minutes: Get-Content -Path C:\FoodTechPOS\logs\app_*.log -Wait
```

### Rollback Procedure (If Upgrade Fails)

```powershell
# Automatic rollback triggered if critical errors detected
# Manual rollback (use most recent pre-upgrade backup):
cd C:\FoodTechPOS\bin\
.\RestoreUtility.exe -mode=full -backup-date=<pre-upgrade-date> -verify=true
Restart-Service FoodTechPOS, FoodTechPOS-Sync
```

---

## Error Codes & Indicators

### Common Error Codes

| Code      | Message                     | Severity | Cause                                     | L1 Resolution                                                 | L2 Escalation                                 |
| --------- | --------------------------- | -------- | ----------------------------------------- | ------------------------------------------------------------- | --------------------------------------------- |
| **E1001** | API Connection Timeout      | ERROR    | Network latency or API server unavailable | Check network connectivity; verify firewall rules             | Contact L2 if persists >10 min                |
| **E1002** | Database Sync Failed        | WARN     | Temporary DB connection loss              | Automatic retry in 5 min; if continues, restart sync service  | Check database logs; verify credentials       |
| **E1003** | Invalid Payment Token       | ERROR    | Payment gateway rejection                 | Verify card details; retry transaction                        | Contact payment processor                     |
| **E1004** | Local Database Corruption   | FATAL    | File system error or unclean shutdown     | Automatic recovery attempted; if failed, escalate immediately | Restore from backup; verify storage integrity |
| **E1005** | Configuration File Missing  | FATAL    | Deleted/moved `config.xml`                | Copy from backup location                                     | Full system restore                           |
| **E2001** | SSL Certificate Expired     | ERROR    | Certificate renewal not performed         | Update Windows date/time; install latest cert bundle          | L2 certificate management                     |
| **E2002** | Encryption Key Mismatch     | FATAL    | Database encrypted with different key     | Check for multi-user environment issues                       | Database recovery / key rotation              |
| **E3001** | Printer Communication Error | WARN     | Receipt printer offline/disconnected      | Verify USB connection; restart printer                        | Check device driver; update firmware          |
| **E4001** | Session Timeout             | WARN     | Idle session exceeded 1 hour              | Re-login required                                             | Normal behavior; no escalation                |
| **E5001** | Insufficient Storage        | WARN     | Disk space <100 MB                        | Archive old logs; clear temp files                            | Expand storage / evaluate retention policy    |

### Indicator Lights & Status Codes

**System Status Panel** (on POS terminal):

- 🟢 **Green:** All systems normal
- 🟡 **Yellow:** Warning (network latency, disk space warning, minor API issues)
- 🔴 **Red:** Critical error (no API connectivity, database unavailable, encryption failure)
- ⚪ **White/Blinking:** Startup/shutdown in progress

---

## Support & Escalation

### Support Contacts

| Role                     | Contact                                          | Availability             | Purpose                                                    |
| ------------------------ | ------------------------------------------------ | ------------------------ | ---------------------------------------------------------- |
| **L1 Support**           | `support@servewell.in` or ext. 5500              | 6 AM–10 PM IST (Mon–Sun) | Basic troubleshooting, password resets, log review         |
| **L2 Support**           | `it-l2@servewell.in`                             | 7 AM–11 PM IST (Mon–Fri) | Advanced troubleshooting, configuration, upgrades          |
| **Emergency/Escalation** | `it-emergency@servewell.in` or +91-124-XXXX-XXXX | 24/7                     | Critical production outages                                |
| **Vendor Support**       | `support@foodtechpos.com`                        | Business hours IST       | Hardware RMA, licensing, major bugs                        |
| **Database Team**        | `database-team@servewell.in`                     | 8 AM–6 PM IST (Mon–Fri)  | Database-specific issues, replication problems             |
| **Security Team**        | `security@servewell.in`                          | 8 AM–6 PM IST (Mon–Fri)  | Security incidents, SSL certificate management, compliance |

### Escalation Procedure

**Level 1 → Level 2:** When troubleshooting does not resolve issue within 15 minutes or issue involves:

- System restart / service restart
- Configuration file modification
- Database restoration
- Any FATAL error code
- Multiple locations affected

**Level 2 → Vendor:** When issue is unresolved after 4 hours or appears to be:

- Hardware defect
- Licensing/activation problem
- Software bug in production code
- Firmware incompatibility

**Escalation to Emergency:** When:

- Multiple locations simultaneously impacted
- Payment processing completely unavailable
- Security breach suspected
- Data loss occurring

**Required Information for All Escalations:**

- Terminal ID and location
- Affected system version
- Error code and full error message
- Steps already attempted
- Time issue first observed
- Impact (single terminal vs. all locations)
- Current backup status

---

## Troubleshooting Quick Reference (L1)

### POS Terminal Won't Start

1. Check power cable and UPS status
2. Verify Windows is booting (wait 3 minutes)
3. Check Windows Event
