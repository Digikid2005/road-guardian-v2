# agent/nodes/make_calls.py
import os, asyncio
from twilio.rest import Client
from urllib.parse import urlencode
from agent.state import AgentState

def get_twilio():
    return Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )

async def make_calls_node(state: AgentState) -> AgentState:
    print('📞 [Node 3] Initiating Twilio voice calls...')
    client     = get_twilio()
    from_num   = os.getenv('TWILIO_FROM_NUMBER')
    twiml_base = os.getenv('TWILIO_TWIML_URL')
    call_results = []

    for hospital in state['ranked_hospitals']:
        # Build TwiML URL with query params
        params = urlencode({
            'hospital': hospital['name'],
            'severity': 'HIGH',
            'distance': hospital['distance_km']
        })
        twiml_url = f'{twiml_base}?{params}'

        try:
            call = client.calls.create(
                to=hospital['phone_number'],
                from_=from_num,
                url=twiml_url,
                timeout=30,            # ring for 30s before giving up
                status_callback=f'{twiml_base}/status',  # optional
            )
            call_results.append({
                'hospital_id': hospital['id'],
                'hospital_name': hospital['name'],
                'priority': hospital['priority'],
                'call_sid': call.sid,
                'status': call.status
            })
            print(f'   ✅ Called {hospital["name"]} — SID: {call.sid}')

        except Exception as e:
            print(f'   ❌ Call to {hospital["name"]} failed: {e}')
            call_results.append({
                'hospital_name': hospital['name'],
                'priority': hospital['priority'],
                'error': str(e)
            })

        # 5-second gap between calls
        await asyncio.sleep(5)

    return {**state, 'call_results': call_results}
