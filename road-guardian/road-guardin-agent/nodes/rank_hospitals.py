# utils/haversine.py
import math

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Returns the great-circle distance in kilometres between two
    geographic coordinates using the Haversine formula.
    Accuracy: ±0.5% — sufficient for emergency routing.
    """
    R = 6371.0  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)

    a = (math.sin(dphi / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))
# agent/nodes/rank_hospitals.py
from utils.haversine import haversine_km
from agent.state import AgentState

async def rank_hospitals_node(state: AgentState) -> AgentState:
    print('📍 [Node 2] Ranking hospitals by distance...')

    accident = state['accident']
    acc_lat  = float(accident['latitude'])
    acc_lon  = float(accident['longitude'])

    # Calculate distance for every hospital
    hospitals_with_dist = []
    for h in state['hospitals']:
        dist = haversine_km(acc_lat, acc_lon,
                            float(h['latitude']),
                            float(h['longitude']))
        hospitals_with_dist.append({**h, 'distance_km': round(dist, 2)})

    # Sort ascending — nearest first
    hospitals_with_dist.sort(key=lambda x: x['distance_km'])

    # Take top 3 and assign priority
    top3 = []
    for i, h in enumerate(hospitals_with_dist[:3]):
        top3.append({**h, 'priority': i + 1})
        print(f'   #{i+1}  {h["name"]} — {h["distance_km"]} km')

    return {**state, 'ranked_hospitals': top3}
