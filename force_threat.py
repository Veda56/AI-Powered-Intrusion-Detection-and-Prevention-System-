import requests
import json
import time
import subprocess

def test_threat_system():
    base_url = "http://192.168.56.1:5000"
    
    print("🔍 TESTING AATIS SECURITY SYSTEM THREAT DETECTION")
    print("=" * 50)
    
    # 1. Check current state
    print("\n1. Checking current system state...")
    response = requests.get(f"{base_url}/api/threats")
    current_threats = response.json()
    print(f"   Current threats: {len(current_threats)}")
    
    response = requests.get(f"{base_url}/api/security/events")
    current_events = response.json()
    print(f"   Security events: {len(current_events)}")
    
    # 2. Test 1: Run network scan
    print("\n2. Testing network scan...")
    response = requests.post(f"{base_url}/api/quick-scan")
    scan_result = response.json()
    print(f"   Scan result: {scan_result}")
    
    # 3. Test 2: Run nmap scan (should trigger process detection)
    print("\n3. Testing nmap process detection...")
    try:
        print("   Running nmap scan...")
        # Run a more extensive nmap scan that takes longer
        process = subprocess.Popen([
            'nmap', '-T4', '-p', '1-100', '--max-retries', '2', '192.168.56.1'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it time to be detected
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("   Nmap is still running (good for detection)")
            process.terminate()
            process.wait(timeout=5)
        else:
            print("   Nmap completed quickly")
            
    except Exception as e:
        print(f"   Nmap error: {e}")
    
    # 4. Test 3: Check system health
    print("\n4. Checking system health...")
    response = requests.get(f"{base_url}/api/system/health")
    health = response.json()
    print(f"   CPU Usage: {health.get('cpu_usage', 'N/A')}%")
    print(f"   Memory Usage: {health.get('memory_usage', 'N/A')}%")
    print(f"   Security Score: {health.get('security_score', 'N/A')}")
    
    # 5. Wait a bit for detection to process
    print("\n5. Waiting for threat detection...")
    time.sleep(5)
    
    # 6. Check final state
    print("\n6. Checking final system state...")
    response = requests.get(f"{base_url}/api/threats")
    final_threats = response.json()
    print(f"   Final threats: {len(final_threats)}")
    
    response = requests.get(f"{base_url}/api/security/events")
    final_events = response.json()
    print(f"   Final events: {len(final_events)}")
    
    # 7. Results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print("=" * 50)
    
    if len(final_threats) > len(current_threats):
        print("✅ THREAT DETECTION WORKING!")
        new_threats = final_threats[len(current_threats):]
        for threat in new_threats:
            print(f"   🚨 New Threat: {threat['type']}")
            print(f"      Description: {threat['description']}")
            print(f"      Severity: {threat['severity']}")
    else:
        print("❌ No new threats detected")
        print("   This means:")
        print("   - Process monitoring may not detect nmap")
        print("   - Detection thresholds may be too high")
        print("   - Nmap runs too quickly to be caught")
    
    # Show new security events
    new_events = final_events[len(current_events):]
    if new_events:
        print(f"\n   New security events: {len(new_events)}")
        for event in new_events[-3:]:  # Show last 3 events
            print(f"   📋 {event['type']}: {event['message']}")
    
    # System status
    print(f"\n💡 SYSTEM STATUS:")
    print(f"   Threats detected: {len(final_threats)}")
    print(f"   Total events: {len(final_events)}")
    print(f"   Security score: {health.get('security_score', 'N/A')}/100")

def test_individual_apis():
    """Test each API endpoint individually"""
    base_url = "http://192.168.56.1:5000"
    
    print("\n" + "=" * 50)
    print("🔧 INDIVIDUAL API TESTS:")
    print("=" * 50)
    
    endpoints = [
        "/api/threats/stats",
        "/api/performance/metrics", 
        "/api/traffic/metrics",
        "/api/network/devices",
        "/api/system/ip"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: OK (data length: {len(str(data))})")
            else:
                print(f"❌ {endpoint}: Error {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Failed - {e}")

if __name__ == "__main__":
    try:
        test_threat_system()
        test_individual_apis()
        
        print("\n" + "=" * 50)
        print("🎯 NEXT STEPS:")
        print("=" * 50)
        print("1. If no threats detected, we need to enhance process monitoring")
        print("2. Check Flask console for 'REAL DETECTION' messages") 
        print("3. May need to modify detection thresholds in app.py")
        print("4. Try running multiple nmap scans quickly")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to AATIS system at http://192.168.56.1:5000")
        print("   Make sure your Flask server is running!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")