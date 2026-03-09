export default function RegistrationModal({ onClose }) {
  function handleSubmit(e) {
    e.preventDefault();
    alert("Hospital Registered Successfully (Demo)");
    onClose();
  }

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>🏥 Hospital Registration</h2>

        <form onSubmit={handleSubmit}>
          <input placeholder="Hospital Name" required />
          <input placeholder="City" required />
          <input placeholder="Contact Number" required />
          <input placeholder="Emergency Email" required />

          <div className="modal-actions">
            <button type="submit">Register</button>
            <button type="button" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
