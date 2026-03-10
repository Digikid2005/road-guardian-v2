# agent/nodes/fetch_hospitals.py
import os
from supabase import create_client
from agent.state import AgentState

def get_supabase():
    return create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_SERVICE_KEY')  # use service key, NOT anon
    )

async def fetch_hospitals_node(state: AgentState) -> AgentState:
    print('🏥 [Node 1] Fetching hospitals from Supabase...')
    try:
        supabase = get_supabase()
        response = supabase.table('hospitals') \
            .select('*') \
            .eq('is_active', True) \
            .execute()

        hospitals = response.data or []
        print(f'   Found {len(hospitals)} active hospitals')
        return {**state, 'hospitals': hospitals}

    except Exception as e:
        print(f'❌ [Node 1] Error: {e}')
        return {**state, 'status': 'failed', 'error': str(e)}
