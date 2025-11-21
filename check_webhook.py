import urllib.request
import json
from config import Config

# Check and delete webhook
bot_token = Config.BOT_TOKEN
print(f"Checking webhook for bot...")

# Get current webhook
with urllib.request.urlopen(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo") as response:
    webhook_info = json.loads(response.read())

print(f"\nWebhook Info:")
print(f"URL: {webhook_info.get('result', {}).get('url', 'None')}")
print(f"Has custom certificate: {webhook_info.get('result', {}).get('has_custom_certificate', False)}")
print(f"Pending update count: {webhook_info.get('result', {}).get('pending_update_count', 0)}")

# Delete webhook to enable long polling
if webhook_info.get('result', {}).get('url'):
    print("\n⚠️ Webhook is set! Deleting it to enable bot updates...")
    with urllib.request.urlopen(f"https://api.telegram.org/bot{bot_token}/deleteWebhook") as delete_response:
        result = json.loads(delete_response.read())
        if result.get('ok'):
            print("✅ Webhook deleted successfully!")
            print("Now the bot should work with long polling.")
        else:
            print(f"❌ Failed to delete webhook: {result}")
else:
    print("\n✅ No webhook set. Bot should be using long polling.")
