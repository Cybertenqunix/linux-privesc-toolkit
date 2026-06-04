#!/usr/bin/env python3
import os
import subprocess
import datetime

# ==========================================
# Linux Privilege Escalation Automation Toolkit
# Mode: Read-Only / Detection Only
# ==========================================

def run_command(cmd):
    """Executes a shell command and returns the output safely."""
    try:
        result = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing command: {e}"

def get_system_info():
    """Gathers basic system and kernel information."""
    print("\n[*] GATHERING SYSTEM INFORMATION...")
    print("-" * 40)
    sys_info = {
        "OS Release": run_command("cat /etc/os-release | grep PRETTY_NAME | cut -d '=' -f 2 | tr -d '\"'"),
        "Kernel Version": run_command("uname -r"),
        "Current User": run_command("whoami"),
        "User ID / Groups": run_command("id")
    }
    
    for key, value in sys_info.items():
        print(f"[+] {key}: {value}")

def check_suid_binaries():
    """Scans for SUID/SGID binaries and checks against high-risk targets."""
    print("\n[*] SCANNING FOR SUID/SGID BINARIES...")
    print("-" * 40)
    # High-risk binaries often found on GTFOBins
    high_risk = ['awk', 'bash', 'cp', 'find', 'nmap', 'perl', 'python', 'vim', 'less', 'more']
    
    # Find SUID binaries (2>/dev/null hides permission denied errors)
    suid_cmd = "find / -perm -4000 -type f 2>/dev/null"
    output = run_command(suid_cmd)
    
    if output:
        binaries = output.split('\n')
        print(f"[!] Found {len(binaries)} SUID binaries.")
        
        for binary in binaries:
            bin_name = binary.split('/')[-1]
            if bin_name in high_risk:
                print(f"  [CRITICAL] High-Risk SUID found: {binary} (Check GTFOBins!)")
    else:
        print("[-] No SUID binaries found or scan failed.")

def check_weak_permissions():
    """Checks for writable critical files like /etc/passwd and /etc/shadow."""
    print("\n[*] CHECKING CRITICAL FILE PERMISSIONS...")
    print("-" * 40)
    critical_files = ['/etc/passwd', '/etc/shadow', '/etc/crontab']
    
    for file in critical_files:
        if os.path.exists(file):
            if os.access(file, os.W_OK):
                print(f"  [CRITICAL] {file} is WRITABLE by the current user!")
            else:
                print(f"  [OK] {file} is secure (Read-only for current user).")
        else:
            print(f"  [-] {file} does not exist.")

def check_sudo_privileges():
    """Analyzes sudo rules for the current user."""
    print("\n[*] ANALYZING SUDO PRIVILEGES (sudo -l)...")
    print("-" * 40)
    sudo_output = run_command("sudo -n -l")
    
    if "password is required" in sudo_output or "a password is required" in sudo_output:
        print("  [-] Sudo requires a password. Cannot check automatically without credentials.")
    elif "NOPASSWD" in sudo_output:
        print("  [CRITICAL] NOPASSWD directive found! User can run the following as root without a password:")
        print(f"      {sudo_output}")
    elif sudo_output:
        print("  [!] Sudo privileges found:")
        print(f"      {sudo_output}")
    else:
        print("  [-] No sudo privileges configured for current user.")

def generate_report():
    """Main execution engine."""
    print("=" * 60)
    print("   LINUX PRIVILEGE ESCALATION AUTOMATION TOOLKIT (LPEAT)")
    print(f"   Scan initiated at: {datetime.datetime.now()}")
    print("=" * 60)
    
    get_system_info()
    check_suid_binaries()
    check_weak_permissions()
    check_sudo_privileges()
    
    print("\n" + "=" * 60)
    print("[*] SCAN COMPLETE. Review the critical tags above for mitigation.")
    print("=" * 60)

if __name__ == "__main__":
    # Ensure script is running on a Linux system
    if os.name != 'posix':
        print("[!] This toolkit is designed strictly for Linux environments.")
        exit(1)
    generate_report()
