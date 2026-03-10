# agent/nodes/send_sms.py
import os, asyncio
from twilio.rest import Client
from datetime import datetime
from agent.state import AgentState

def format_sms(accident: dict, hospital: dict) -> str:
    """Builds the SMS body sent to each hospital."""
    ts = accident.get('created_at', '')
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        ts_fmt = dt.strftime('%d %b %Y  %H:%M:%S UTC')
    except Exception:
        ts_fmt = ts

    lat = accident.get('latitude', 'N/A')
    lon = accident.get('longitude', 'N/A')
    maps_url = f'https://maps.google.com/?q={lat},{lon}'

    return (
        f'🚨 ROAD GUARDIAN — EMERGENCY ALERT\n'
        f'Priority #{hospital["priority"]} | {hospital["distance_km"]} km away\n'
        f'━━━━━━━━━━━━━━━━━━━━━━━\n'
        f'ID:       {accident.get("id", "N/A")}\n'
        f'Vehicle:  {accident.get("vehicle_number", "N/A")}\n'
        f'Victim:   {accident.get("name", "N/A")}\n'
        f'Phone:    {accident.get("phone_number", "N/A")}\n'
        f'Time:     {ts_fmt}\n'
        f'━━━━━━━━━━━━━━━━━━━━━━━\n'
        f'GPS: {lat}, {lon}\n'
        f'MAP: {maps_url}\n'
        f'━━━━━━━━━━━━━━━━━━━━━━━\n'
        f'Reply CLAIM to accept this emergency.'
    )

async def send_sms_node(state: AgentState) -> AgentState:
    print('💬 [Node 4] Sending Twilio SMS...')
    client   = get_twilio()
    from_num = os.getenv('TWILIO_FROM_NUMBER')
    sms_results = []

    for hospital in state['ranked_hospitals']:
        body = format_sms(state['accident'], hospital)
        try:
            msg = client.messages.create(
                to=hospital['phone_number'],
                from_=from_num,
                body=body
            )
            sms_results.append({
                'hospital_name': hospital['name'],
                'priority': hospital['priority'],
                'message_sid': msg.sid,
                'status': msg.status
            })
            print(f'   ✅ SMS → {hospital["name"]} — SID: {msg.sid}')

        except Exception as e:
            print(f'   ❌ SMS to {hospital["name"]} failed: {e}')
            sms_results.append({
                'hospital_name': hospital['name'],
                'error': str(e)
            })

        await asyncio.sleep(1)  # small delay

    return {**state, 'sms_results': sms_results}

def get_twilio():
    return Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
