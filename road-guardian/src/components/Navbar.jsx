import { useState } from "react";
import RegistrationModal from "./RegistrationModal";

export default function Navbar() {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <nav className="navbar">
        <h1>🚑 Road Guardian</h1>
        <button onClick={() => setShowModal(true)}>
          Hospital Registration
        </button>
      </nav>

      {showModal && (
        <RegistrationModal onClose={() => setShowModal(false)} />
      )}
    </>
  );
}
