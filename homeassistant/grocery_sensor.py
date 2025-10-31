"""
AppDaemon Grocery Sensor - FD-safe implementation
Polls grocery API every 60s and updates Home Assistant sensor
"""
import appdaemon.plugins.hass.hassapi as hass
import requests
from datetime import datetime


class GrocerySensor(hass.Hass):
    """Fetch latest grocery purchase and update HA sensor."""

    def initialize(self):
        """Setup session and start polling."""
        self.api_url = self.args.get("api_url", "http://192.168.178.123:8082/api")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "HomeAssistant-GrocerySensor/1.0",
            "Accept": "application/json"
        })
        
        # Delayed start to avoid startup congestion
        self.run_in(self.start_polling, 5)
        self.log("GrocerySensor initialized, starting in 5s")

    def start_polling(self, kwargs):
        """Start periodic polling."""
        self.run_every(self.fetch_grocery_data, "now", 60)
        self.log("Polling started (60s interval)")

    def fetch_grocery_data(self, kwargs):
        """Fetch latest purchase from API and update sensor."""
        try:
            # HTTP request with timeout
            response = self.session.get(
                f"{self.api_url}/purchase/history?limit=1",
                timeout=(5, 15)  # connect, read timeout
            )
            response.raise_for_status()
            data = response.json()
            
            if not data or len(data) == 0:
                self.log("No purchase data available", level="WARNING")
                return
            
            # Get latest purchase
            purchase = data[0]
            
            # Calculate total price
            total_cents = sum(
                item.get("price_cents_at_purchase", 0) * item.get("qty", 1)
                for item in purchase.get("items", [])
            )
            
            # Format state (ISO timestamp)
            state = purchase.get("purchased_at", "unknown")
            
            # Build attributes
            attributes = {
                "supermarket_id": purchase.get("supermarket_id", "unknown"),
                "items_count": len(purchase.get("items", [])),
                "total_price_cents": total_cents,
                "total_price_euro": round(total_cents / 100, 2),
                "products": [
                    item.get("product", {}).get("name", "unknown")
                    for item in purchase.get("items", [])[:10]  # Top 10
                ],
                "last_update": datetime.now().isoformat()
            }
            
            # Update HA sensor
            self.set_state(
                "sensor.last_grocery_purchase",
                state=state,
                attributes=attributes
            )
            
            self.log(f"✓ Updated: {len(purchase.get('items', []))} items, {attributes['total_price_euro']}€")
            
        except requests.Timeout:
            self.log("API timeout (>15s)", level="WARNING")
        except requests.RequestException as e:
            self.log(f"API error: {e}", level="ERROR")
        except Exception as e:
            self.log(f"Unexpected error: {e}", level="ERROR")

    def terminate(self):
        """Cleanup session on shutdown."""
        if hasattr(self, 'session') and self.session:
            self.session.close()
            self.log("Session closed")


# FD-Summary:
# - Öffnet Netzwerk? ja (HTTP)
# - Session wiederverwendet? ja
# - Subprocess? nein
# - Empfohlenes Intervall: 60s (konfiguriert)
# - Cleanup vorhanden? ja (terminate)
