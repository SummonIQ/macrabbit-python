import os
import subprocess
from typing import Dict, Optional, Tuple
import shlex
import psutil

def get_uid() -> int:
    """Get the current user's UID."""
    return os.getuid()

def parse_launchctl_print_output(output: str) -> Tuple[set, Dict[str, str]]:
    """Parse the output of launchctl print-disabled to get disabled services."""
    disabled = set()
    status_map = {}
    for line in output.splitlines():
        if '=>' in line:
            parts = line.strip().split('=>')
            if len(parts) == 2:
                name = parts[0].strip().strip('"')
                status = parts[1].strip()
                if status == 'disabled':
                    disabled.add(name)
                status_map[name] = status
    return disabled, status_map

def get_service_details(service_name: str, service_type: str, statuses: Dict[str, str], pids: Dict[str, str]) -> Optional[Dict]:
    """Get details for a specific service."""
    status = statuses.get(service_name, 'enabled')
    pid = pids.get(service_name)
    return {
        'status': 'running' if pid else status,
        'pid': pid,
        'type': service_type,
    }

def get_live_services(console=None) -> Dict[str, Dict[str, Dict]]:
    """Get the current status of all services."""
    from .service_database import SERVICE_DATABASE
    
    uid = get_uid()
    
    # Get running services (user agents)
    try:
        user_services_result = subprocess.run(["launchctl", "list"], capture_output=True, text=True, check=True)
        user_pids = {}
        for line in user_services_result.stdout.splitlines():
            if line.strip() and not line.startswith('PID'):
                parts = line.split()
                if len(parts) >= 3:
                    pid = parts[0]
                    service_name = parts[2]
                    if pid != '-':
                        user_pids[service_name] = pid
    except subprocess.CalledProcessError:
        user_pids = {}
    
    # Get running services (system daemons)
    try:
        system_services_result = subprocess.run(["sudo", "launchctl", "list"], capture_output=True, text=True, check=True)
        system_pids = {}
        for line in system_services_result.stdout.splitlines():
            if line.strip() and not line.startswith('PID'):
                parts = line.split()
                if len(parts) >= 3:
                    pid = parts[0]
                    service_name = parts[2]
                    if pid != '-':
                        system_pids[service_name] = pid
    except subprocess.CalledProcessError:
        system_pids = {}
    
    # Get disabled services (user agents)
    try:
        user_disabled_result = subprocess.run(["launchctl", "print-disabled", f"gui/{uid}"], capture_output=True, text=True, check=True)
        user_disabled, _ = parse_launchctl_print_output(user_disabled_result.stdout)
    except subprocess.CalledProcessError:
        user_disabled = set()
    
    # Get disabled services (system daemons)
    try:
        system_disabled_result = subprocess.run(["sudo", "launchctl", "print-disabled", "system"], capture_output=True, text=True, check=True)
        system_disabled, _ = parse_launchctl_print_output(system_disabled_result.stdout)
    except subprocess.CalledProcessError:
        system_disabled = set()
    
    # Organize services by category
    services_by_category = {}
    
    for service_name, service_info in SERVICE_DATABASE.items():
        # Determine service type and status
        if service_name in system_pids:
            service_type = "daemon"
            status = "running"
        elif service_name in user_pids:
            service_type = "agent"
            status = "running"
        elif service_name in system_disabled:
            service_type = "daemon"
            status = "disabled"
        elif service_name in user_disabled:
            service_type = "agent"
            status = "disabled"
        else:
            # Default to agent if not found
            service_type = "agent"
            status = "enabled"
        
        # Create service entry
        service_entry = {
            "description": service_info["description"],
            "impact": service_info["impact"],
            "status": status,
            "type": service_type
        }
        
        # Categorize service
        category = categorize_service(service_name)
        if category not in services_by_category:
            services_by_category[category] = {}
        
        services_by_category[category][service_name] = service_entry
    
    return services_by_category

def categorize_service(service_name: str) -> str:
    """Categorize a service by its name."""
    # Define service categories based on your TUI categories
    categories = {
        "🔍 Advertising & Analytics": [
            "com.apple.ap.adprivacyd", "com.apple.ap.promotedcontentd", "com.apple.adid",
            "com.apple.parsec-fbf", "com.apple.analyticsd", "com.apple.osanalytics.osanalyticshelper",
            "com.apple.symptomsd", "com.apple.wifianalyticsd", "com.apple.audioanalyticsd",
            "com.apple.ecosystemanalyticsd", "com.apple.perfpowermetricd", "com.apple.metrickitd",
            "com.apple.analyticsagent", "com.apple.dprivacyd", "com.apple.PerfPowerTelemetryClientRegistrationService",
            "com.apple.memoryanalyticsd", "com.apple.inputanalyticsd", "com.apple.geoanalyticsd"
        ],
        "🛒 App & Store Related": [
            "com.apple.appstoreagent", "com.apple.appstored", "com.apple.commerce",
            "com.apple.passd", "com.apple.financed", "com.apple.watchlistd",
            "com.apple.triald.system", "com.apple.newsd", "com.apple.appinstalld",
            "com.apple.assetsubscriptiond", "com.apple.bookassetd", "com.apple.storeaccountd",
            "com.apple.storeuid", "com.apple.storedownloadd", "com.apple.appsleep",
            "com.apple.storekitagent", "com.apple.appplaceholdersyncd", "com.apple.askpermissiond",
            "com.apple.amsondevicestoraged", "com.apple.amsaccountsd", "com.apple.amsengagementd",
            "com.apple.AppStoreDaemon.StorePrivilegedODRService", "com.apple.AppStoreDaemon.StorePrivilegedTaskService",
            "com.apple.eligibilityd", "com.apple.fairplayd", "com.apple.fairplaydeviceidentityd",
            "com.apple.storereceiptinstaller"
        ],
        "🔌 Hardware & Drivers": [
            "com.apple.touchbarserver", "com.apple.controlstrip"
        ],
        "🗣️ Siri & Dictation": [
            "com.apple.assistantd", "com.apple.corespeechd", "com.apple.siriknowledged",
            "com.apple.Siri.agent", "com.apple.shazamd", "com.apple.speech.speechsynthesisd",
            "com.apple.speech.synthesisserver", "com.apple.speech.speechdatainstallerd",
            "com.apple.DictationIM", "com.apple.corespeechd_system", "com.apple.siri.acousticsignature",
            "com.apple.assistant_service", "com.apple.siriactionsd", "com.apple.SiriTTSTrainingAgent",
            "com.apple.sirittsd", "com.apple.siri.context.service", "com.apple.speech.speechsynthesisd.x86_64",
            "com.apple.SpeechRecognitionCore.brokerd"
        ]
    }
    
    for category, services in categories.items():
        if service_name in services:
            return category
    
    return "🔧 Other Services"

def run_with_admin_privileges(cmd):
    """Run a shell command with admin privileges using osascript for a native password prompt."""
    # Escape the command for AppleScript
    cmd_str = ' '.join(shlex.quote(str(c)) for c in cmd)
    osa_cmd = [
        'osascript',
        '-e', f'do shell script "{cmd_str}" with administrator privileges'
    ]
    return subprocess.run(osa_cmd, capture_output=True, text=True)

def bootout_and_disable(service, uid):
    """Boots out and disables a user agent, returns (success, error_message)"""
    bootout_cmd = ["launchctl", "bootout", f"gui/{uid}/{service}"]
    disable_cmd = ["launchctl", "disable", f"gui/{uid}/{service}"]
    bootout_result = subprocess.run(bootout_cmd, capture_output=True, text=True)
    disable_result = subprocess.run(disable_cmd, capture_output=True, text=True)
    check_disabled = subprocess.run(["launchctl", "print-disabled", f"gui/{uid}"], capture_output=True, text=True)
    is_disabled = f'"{service}" => disabled' in check_disabled.stdout
    check_running = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
    is_running = any(service in line and not line.strip().startswith('-') for line in check_running.stdout.splitlines())
    if is_disabled and not is_running:
        return True, ""
    else:
        msg = []
        if not is_disabled:
            msg.append("Service is not marked as disabled.")
        if is_running:
            msg.append("Service is still running.")
        if bootout_result.returncode != 0:
            msg.append(f"bootout error: {bootout_result.stderr.strip()}")
        if disable_result.returncode != 0:
            msg.append(f"disable error: {disable_result.stderr.strip()}")
        return False, " ".join(msg)

def bootout_and_disable_system_daemon(service):
    """Boots out and disables a system daemon, returns (success, error_message)"""
    bootout_cmd = ["launchctl", "bootout", f"system/{service}"]
    disable_cmd = ["launchctl", "disable", f"system/{service}"]
    bootout_result = run_with_admin_privileges(bootout_cmd)
    disable_result = run_with_admin_privileges(disable_cmd)
    check_disabled = run_with_admin_privileges(["launchctl", "print-disabled", "system"])
    is_disabled = f'"{service}" => disabled' in check_disabled.stdout
    check_running = run_with_admin_privileges(["launchctl", "list"])
    is_running = any(service in line and not line.strip().startswith('-') for line in check_running.stdout.splitlines())
    if is_disabled and not is_running:
        return True, ""
    else:
        msg = []
        if not is_disabled:
            msg.append("Service is not marked as disabled.")
        if is_running:
            msg.append("Service is still running.")
        if bootout_result.returncode != 0:
            msg.append(f"bootout error: {bootout_result.stderr.strip()}")
        if disable_result.returncode != 0:
            msg.append(f"disable error: {disable_result.stderr.strip()}")
        return False, " ".join(msg)

def check_sip_status() -> bool:
    """Check if System Integrity Protection (SIP) is enabled."""
    try:
        result = subprocess.run(["csrutil", "status"], capture_output=True, text=True, check=True)
        return "System Integrity Protection status: enabled" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return True

def get_process_list():
    """Return a list of running processes with name, PID, CPU, memory, and nice value."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'nice', 'username']):
        try:
            info = proc.info
            processes.append({
                'name': info['name'],
                'pid': info['pid'],
                'cpu': info['cpu_percent'],
                'memory': info['memory_info'].rss // (1024 * 1024),  # MB
                'nice': info['nice'],
                'username': info['username'],
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def is_critical_process(name):
    critical = {'WindowServer', 'kernel_task', 'launchd', 'syslogd', 'systemstats', 'loginwindow'}
    return name in critical

def change_process_priority(pid, new_nice):
    """Change the nice value of a process. Uses osascript for sudo if needed. Returns (success, error_message)."""
    import subprocess
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        if is_critical_process(name):
            return False, f"Cannot change priority of critical system process: {name}"
        current_nice = proc.nice()
        if proc.username() != psutil.Process().username() or pid == 1:
            # Use osascript for sudo renice
            cmd = ["renice", str(new_nice), "-p", str(pid)]
            cmd_str = ' '.join(shlex.quote(str(c)) for c in cmd)
            osa_cmd = [
                'osascript',
                '-e', f'do shell script "{cmd_str}" with administrator privileges'
            ]
            result = subprocess.run(osa_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return False, result.stderr.strip() or result.stdout.strip()
        else:
            proc.nice(new_nice)
        return True, ""
    except Exception as e:
        return False, str(e) 