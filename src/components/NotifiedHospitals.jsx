// src/components/NotifiedHospitals.jsx
export default function NotifiedHospitals({ notifiedHospitals, status }) {
    if (!notifiedHospitals) return null;
  
    const hospitals = typeof notifiedHospitals === 'string'
      ? JSON.parse(notifiedHospitals)
      : notifiedHospitals;
  
    return (
      <div className='notified-hospitals'>
        <h3>
          {status === 'notified' ? '✅ Hospitals Alerted' : '⏳ Alerting...'} 
        </h3>
        {hospitals.map((h) => (
          <div key={h.name} className='hospital-row'>
            <span className='priority'>#{h.priority}</span>
            <span className='name'>{h.name}</span>
            <span className='dist'>{h.distance_km} km</span>
          </div>
        ))}
      </div>
    );
  }
  