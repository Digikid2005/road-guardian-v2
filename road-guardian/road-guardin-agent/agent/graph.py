# agent/graph.py
from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.fetch_hospitals import fetch_hospitals_node
from agent.nodes.rank_hospitals  import rank_hospitals_node
from agent.nodes.make_calls      import make_calls_node
from agent.nodes.send_sms        import send_sms_node
from agent.nodes.update_status   import update_status_node

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # ── Register nodes ──
    graph.add_node('fetch_hospitals',  fetch_hospitals_node)
    graph.add_node('rank_hospitals',   rank_hospitals_node)
    graph.add_node('make_calls',       make_calls_node)
    graph.add_node('send_sms',         send_sms_node)
    graph.add_node('update_status',    update_status_node)

    # ── Define edges (linear pipeline) ──
    graph.set_entry_point('fetch_hospitals')
    graph.add_edge('fetch_hospitals', 'rank_hospitals')
    graph.add_edge('rank_hospitals',  'make_calls')
    graph.add_edge('make_calls',      'send_sms')
    graph.add_edge('send_sms',        'update_status')
    graph.add_edge('update_status',   END)

    return graph.compile()
