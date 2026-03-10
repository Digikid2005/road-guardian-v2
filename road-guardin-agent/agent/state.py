# agent/state.py
from typing import TypedDict, List, Optional

class HospitalWithDistance(TypedDict):
    id: str
    name: str
    address: str
    phone_number: str
    latitude: float
    longitude: float
    distance_km: float    # computed by rank node
    priority: int         # 1 = nearest, 2, 3

class AgentState(TypedDict):
    accident: dict                        # raw Supabase accident record
    hospitals: List[dict]                 # all hospitals from DB
    ranked_hospitals: List[HospitalWithDistance]  # sorted by distance
    call_results: List[dict]              # Twilio call SIDs
    sms_results:  List[dict]              # Twilio SMS SIDs
    status: str                           # running | completed | failed
    error: Optional[str]                  # error message if any
