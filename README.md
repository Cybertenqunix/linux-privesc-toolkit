# Linux Privilege Escalation Automation Toolkit (LPEAT)

## 🛡️ Project Overview
The **Linux Privilege Escalation Automation Toolkit (LPEAT)** is a read-only, automated security auditing script designed for Linux environments. It simulates red-team enumeration techniques to identify system misconfigurations that could lead to unauthorized privilege escalation, while providing blue-team defenders with actionable data for remediation.

This project was built to demonstrate practical knowledge of Linux permissions, SUID/SGID behaviors, cron job vulnerabilities, and secure system configuration.

## ✨ Core Features
- **System Profiling:** Captures OS release, kernel version, and active user context.
- **SUID/SGID Discovery:** Scans the filesystem for binaries with SUID bits set and cross-references them with known high-risk GTFOBins attack vectors (e.g., `find`, `vim`, `awk`).
- **Weak Permission Auditing:** Verifies read/write access controls on critical system files (e.g., `/etc/passwd`, `/etc/shadow`).
- **Sudo Misconfiguration Detection:** Analyzes `sudo -l` rules to detect dangerous `NOPASSWD` directives.
- **Safe Execution:** Operates strictly in a "Detection Only" mode. It does not execute exploits or alter system states.

## 🚀 Installation & Usage

**Prerequisites:** Python 3.x, Linux OS.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/linux-privesc-toolkit.git](https://github.com/YOUR_USERNAME/linux-privesc-toolkit.git)
   cd linux-privesc-toolkit
