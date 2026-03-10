export default function IncidentPanel({ incidentData }) {
  const { patient, medicalFlags, incident, emergencyContact, claimedBy } =
    incidentData;

  const minutesAgo = Math.floor(
    (Date.now() - incident.crashTime) / 60000
  );

  return (
    <div className="panel locked-state">
      <h2> Patient</h2>
      <p><b>{patient.name}</b> | {patient.age} | {patient.sex}</p>

      <h3> Critical Flags</h3>
      <p> Blood Group: <b>{medicalFlags.bloodGroup}</b></p>
      <p>Allergies: <b>{medicalFlags.allergies ? "Yes" : "No"}</b></p>
      <p>Blood Thinners: <b>{medicalFlags.bloodThinners ? "Yes" : "No"}</b></p>
      <p>Pregnant: <b>{medicalFlags.pregnant}</b></p>

      <h3>Incident</h3>
      <p>Severity: <b>{incident.severity}</b></p>
      <p>Vehicle: <b>{incident.vehicleType}</b></p>
      <p>Crash: <b>{minutesAgo} min ago</b></p>

      <h3>Emergency Contact</h3>
      <p>{emergencyContact.name}</p>
      <p>{emergencyContact.phone}</p>

      <p className="locked">Claimed by {claimedBy}</p>
    </div>
  );
}
