# agent/nodes/update_status.py
import os, json
from supabase import create_client
from agent.state import AgentState

async def update_status_node(state: AgentState) -> AgentState:
    print('📝 [Node 5] Updating Supabase accident status...')
    supabase = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_SERVICE_KEY')
    )

    accident_id = state['accident']['id']
    update_payload = {
        'status': 'notified',
        'notified_hospitals': json.dumps([
            {
                'name':        h['name'],
                'priority':    h['priority'],
                'distance_km': h['distance_km'],
            }
            for h in state['ranked_hospitals']
        ])
    }

    # Add notified_hospitals JSONB column to accidents table first:
    # ALTER TABLE accidents ADD COLUMN notified_hospitals JSONB;

    supabase.table('accidents') \
        .update(update_payload) \
        .eq('id', accident_id) \
        .execute()

    print(f'   ✅ Accident {accident_id} marked as notified')
    return {**state, 'status': 'completed'}
