# main.py
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, Response
import os, asyncio
from dotenv import load_dotenv
from agent.graph import build_graph
from agent.state import AgentState

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
    return JSONResponse({'status': 'agent_started', 'id': accident['id']})

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

# TwiML endpoint — Twilio fetches this for call instructions
@app.get('/twiml')
async def twiml_response(hospital: str = '', severity: str = 'HIGH'):
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Pause length="1"/>
      <Say voice="Polly.Joanna" rate="90%">
        This is an automated emergency alert from Road Guardian.
        A road accident has been detected requiring immediate response.
        Severity level: {severity}.
        Hospital {hospital}, please prepare your emergency team.
        This message will repeat once.
      </Say>
      <Pause length="1"/>
      <Say voice="Polly.Joanna" rate="90%">
        This is an automated emergency alert from Road Guardian.
        Severity level: {severity}. Hospital {hospital}, please respond.
      </Say>
    </Response>'''
    return Response(content=xml, media_type='application/xml')

@app.get('/health')
async def health(): return {'status': 'ok'}
