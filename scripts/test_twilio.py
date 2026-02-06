from app.services.notification import NotificationService
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    print("Initializing NotificationService...")
    notifier = NotificationService()
    print("Service Initialized.")
    
    if notifier.client:
        print(f"Twilio Client Active. Account: {notifier.client.username}")
    else:
        print("Twilio Client MISSING (Mock Mode). check .env")

    print("\nAttempting to send invite...")
    # Use a dummy number or safe number if known, or just check instantiation
    res = notifier.send_invite("+15005550006", "Test Group", "http://test.link") # +15005550006 is Twilio Magic Number for 'valid'
    print(f"Result: {res}")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
