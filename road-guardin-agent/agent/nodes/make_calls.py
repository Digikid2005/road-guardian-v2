# agent/nodes/make_calls.py
import os
import asyncio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from agent.state import AgentState


# ─────────────────────────────────────────────
# HARDCODED AUDIO URL
# Replace this with your publicly accessible audio file URL.
# Supported formats: MP3, WAV, AIFF, GSM, μ-law
# The file MUST be reachable by Twilio's servers over HTTPS.
# Example sources: GitHub raw URL, S3 public object, Cloudflare R2 public bucket
# ─────────────────────────────────────────────
EMERGENCY_AUDIO_URL = "https://vxxenzygxzkejqqronbv.supabase.co/storage/v1/object/public/audio/alert.mp3"


def get_twilio_client() -> Client:
    """Initialize and return Twilio REST client."""
    return Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN"),
    )


def build_twiml(hospital_name: str, distance_km: float, severity: str = "HIGH") -> str:
    """
    Build inline TwiML XML string.

    Twilio executes this immediately when the call is answered.
    Using the inline `twiml` parameter in client.calls.create() means
    Twilio does NOT need to make a callback request to your server.

    Audio file at EMERGENCY_AUDIO_URL is played first,
    followed by a spoken summary with hospital-specific details.
    """
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Pause length="1"/>
  <Play>{EMERGENCY_AUDIO_URL}</Play>
  <Pause length="1"/>
  <Say voice="Polly.Joanna" rate="90%">
    Hospital {hospital_name}, severity level {severity}.
    Distance from accident: {distance_km} kilometres.
    Please prepare your emergency team and respond immediately.
    This alert will not repeat. Thank you.
  </Say>
  <Pause length="1"/>
</Response>"""
    return twiml


async def make_calls_node(state: AgentState) -> AgentState:
    """
    Node 3 — Place outbound voice calls to top-3 ranked hospitals via Twilio.

    Uses inline TwiML (no external URL required for call instructions).
    Audio is served from EMERGENCY_AUDIO_URL (hardcoded public URL).
    Calls are placed sequentially with a 5-second gap between each.
    """
    print("📞 [Node 3] Initiating Twilio voice calls...")

    client      = get_twilio_client()
    from_num    = os.getenv("TWILIO_FROM_NUMBER")
    call_results = []

    for hospital in state["ranked_hospitals"]:
        hospital_name = hospital["name"]
        distance_km   = hospital["distance_km"]
        priority      = hospital["priority"]
        to_number     = hospital["phone_number"]

        twiml_xml = build_twiml(
            hospital_name=hospital_name,
            distance_km=distance_km,
            severity="HIGH",
        )

        try:
            call = client.calls.create(
                to=to_number,
                from_=from_num,
                twiml=twiml_xml,   # Inline TwiML — no URL callback needed
                timeout=30,        # Ring for max 30 seconds before giving up
            )

            call_results.append({
                "hospital_id":   hospital["id"],
                "hospital_name": hospital_name,
                "priority":      priority,
                "call_sid":      call.sid,
                "status":        "initiated",
            })
            print(f"   ✅ Called {hospital_name} (Priority #{priority}) — SID: {call.sid}")

        except TwilioRestException as e:
            print(f"   ❌ Twilio call to {hospital_name} failed: {e.msg}")
            call_results.append({
                "hospital_name": hospital_name,
                "priority":      priority,
                "error":         e.msg,
                "status":        "failed",
            })

        except Exception as e:
            print(f"   ❌ Unexpected error calling {hospital_name}: {e}")
            call_results.append({
                "hospital_name": hospital_name,
                "priority":      priority,
                "error":         str(e),
                "status":        "failed",
            })

        # 5-second gap between calls (same as original behaviour)
        await asyncio.sleep(5)

    return {**state, "call_results": call_results}