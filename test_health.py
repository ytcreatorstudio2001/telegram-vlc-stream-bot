#!/usr/bin/env python3
"""
Quick health check script to test if the bot server is running correctly.
Run this after starting the bot to verify it's working.
"""

import requests
import sys

def test_health_endpoint(url="http://localhost:8080"):
    """Test the health endpoint of the bot server."""
    try:
        print(f"🔍 Testing health endpoint: {url}/")
        response = requests.get(f"{url}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check PASSED!")
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Health check FAILED!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error!")
        print("   The server is not running or not accessible.")
        print("   Make sure you've started the bot with: python main.py")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ Timeout Error!")
        print("   The server took too long to respond.")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("🤖 Telegram Stream Bot - Health Check")
    print("=" * 60)
    
    # Test local server
    if test_health_endpoint("http://localhost:8080"):
        print("\n✨ Your bot is running correctly!")
        print("\n📝 Next steps:")
        print("   1. Open Telegram and send /start to your bot")
        print("   2. Send a video/audio file to test streaming")
        print("   3. Copy the generated link and test in VLC")
        sys.exit(0)
    else:
        print("\n⚠️  Bot is not running or has issues.")
        print("\n📝 Troubleshooting:")
        print("   1. Make sure you've filled in .env file")
        print("   2. Run: python main.py")
        print("   3. Check for any error messages")
        print("   4. Wait a few seconds and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()
