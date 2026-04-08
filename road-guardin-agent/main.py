# main.py
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, Response
import os, asyncio
from dotenv import load_dotenv
from agent.graph import build_graph
from agent.state import AgentState
from agent.nodes.make_calls import build_twiml

load_dotenv()
app = FastAPI(title='Road Guardian Agent')

@app.post('/webhook/accident')
async def accident_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    # Validate webhook secret from header
    secret = request.headers.get('x-webhook-secret', '')
    if secret != os.getenv('WEBHOOK_SECRET'):
        raise HTTPException(status_code=401, detail='Unauthorized')

    payload = await request.json()
    accident = payload.get('record', {})  # Supabase sends 'record'

    # Only process new 'pending' accidents
    if not accident or accident.get('status') != 'pending':
        return JSONResponse({'status': 'skipped'})

    # Run agent in background (non-blocking — Supabase times out at 5s)
    background_tasks.add_task(run_agent, accident)
    return JSONResponse({'status': 'agent_started', 'id': accident.get('id')})

async def run_agent(accident: dict):
    graph = build_graph()
    initial_state = AgentState(
        accident=accident,
        hospitals=[],
        ranked_hospitals=[],
        call_results=[],
        sms_results=[],
        status='running'
    )
    result = await graph.ainvoke(initial_state)
    print(f'Agent completed for accident {accident["id"]}: {result["status"]}')

# ── /twiml is now a test/fallback endpoint only ──
# The live call flow uses inline TwiML in make_calls.py (no URL fetch needed).
# You can hit GET /twiml?hospital=TestHospital&severity=HIGH&distance=3.2 to preview the XML.
@app.api_route('/twiml', methods=['GET', 'POST'])
async def twiml_response(hospital: str = 'Unknown', severity: str = 'HIGH', distance: float = 0.0):
    xml = build_twiml(hospital_name=hospital, distance_km=distance, severity=severity)
    return Response(content=xml, media_type='application/xml')

@app.get('/health')
async def health(): 
    return {'status': 'ok'}