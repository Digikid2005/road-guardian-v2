import { useEffect, useState } from "react";
import Navbar from "./components/Navbar";
import MapView from "./components/MapView";
import IncidentPanel from "./components/IncidentPanel";
import { supabase } from "./supabaseClient";

export default function App() {
  const [incidents, setIncidents] = useState([]);
  const [activeIncident, setActiveIncident] = useState(null);

useEffect(() => {
  fetchIncidents(); // initial load

  const channel = supabase
    .channel("accidents-live")
    .on(
      "postgres_changes",
      {
        event: "INSERT",
        schema: "public",
        table: "accidents",
      },
      (payload) => {
        console.log("🔥 REALTIME INSERT:", payload.new);

        setIncidents((prev) => {
          // avoid duplicates
          const exists = prev.find((i) => i.id === payload.new.id);
          if (exists) return prev;

          return [payload.new, ...prev];
        });
      }
    )
    .on('postgres_changes', {
      event: 'UPDATE', schema: 'public', table: 'accidents'   // NEW
    }, (payload) => {
      setIncidents(prev =>
        prev.map(i => i.id === payload.new.id ? payload.new : i)
      );
      // If activeIncident updated, refresh it too
      if (activeIncident?.id === payload.new.id) {
        setActiveIncident(payload.new);
      }
    })  
    .subscribe((status) => {
      console.log("Realtime status:", status);
    });

  return () => {
    supabase.removeChannel(channel);
  };
}, []);


async function fetchIncidents() {
  const { data, error } = await supabase
    .from("accidents")
    .select("*");

  console.log("DATA:", data);
  console.log("ERROR:", error);

  setIncidents(data || []);
}


  // 3️⃣ Claim logic
  async function claimIncident(incident) {
    setActiveIncident(incident);
    setIncidents([]);

    await supabase
      .from("accidents")
      .update({ status: "claimed" })
      .eq("id", incident.id);
  }

  return (
    <>
      <Navbar />

      <div className="app">
        {activeIncident ? (
          <>
            <MapView
              incident={{
                hospitalLocation: [20.2961, 85.8245],
                accidentLocation: [
                  activeIncident.latitude,
                  activeIncident.longitude,
                ],
                ambulanceLocation: [20.2961, 85.8245],
              }}
            />

            <IncidentPanel
              incidentData={{
                patient: {
                  name: activeIncident.name,
                  age: "NA",
                  sex: "NA",
                },
                medicalFlags: {
                  bloodGroup: "NA",
                  allergies: false,
                  bloodThinners: false,
                  pregnant: "NA",
                },
                incident: {
                  severity: "HIGH",
                  vehicleType: "Unknown",
                  crashTime: new Date(activeIncident.created_at).getTime(),
                  status: "LOCKED",
                },
                emergencyContact: {
                  name: "Emergency Contact",
                  phone: activeIncident.phone_number,
                },
                claimedBy: "Hospital A",
              }}
            />
          </>
        ) : (
          <div className="incident-list">
            <h2>🚨 Active Accidents</h2>

            {incidents.map((inc) => (
              <div key={inc.id} className="incident-card">
                <p><b>Vehicle:</b> {inc.vehicle_number}</p>
                <p><b>Victim:</b> {inc.name}</p>
                <button onClick={() => claimIncident(inc)}>
                  CLAIM
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
