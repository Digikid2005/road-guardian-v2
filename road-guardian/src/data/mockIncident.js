export const mockIncidents = [
  {
    id: "INC001",
    patient: {
      name: "Rahul S.",
      age: 28,
      sex: "Male",
    },
    medicalFlags: {
      bloodGroup: "O+",
      allergies: false,
      bloodThinners: false,
      pregnant: "NA",
    },
    incident: {
      severity: "HIGH",
      vehicleType: "Two-Wheeler",
      crashTime: Date.now() - 4 * 60000,
      status: "OPEN",
    },
    emergencyContact: {
      name: "Ashis Kumar Singh",
      phone: "+91 XXXXX XXXXX",
    },
    hospitalLocation: [20.2961, 85.8245],
    accidentLocation: [20.3005, 85.8200],
    ambulanceLocation: [20.2961, 85.8245],
    claimedBy: null,
  },

  {
    id: "INC002",
    patient: {
      name: "Priya M.",
      age: 32,
      sex: "Female",
    },
    medicalFlags: {
      bloodGroup: "B+",
      allergies: true,
      bloodThinners: false,
      pregnant: "No",
    },
    incident: {
      severity: "MODERATE",
      vehicleType: "Car",
      crashTime: Date.now() - 7 * 60000,
      status: "OPEN",
    },
    emergencyContact: {
      name: "Ramesh M.",
      phone: "+91 XXXXX XXXXX",
    },
    hospitalLocation: [20.2961, 85.8245],
    accidentLocation: [20.3021, 85.8260],
    ambulanceLocation: [20.2961, 85.8245],
    claimedBy: null,
  },
  {
    id: "INC003",
    patient: {
      name: "Amit K.",
      age: 45,
      sex: "Male",
    },
    medicalFlags: {
      bloodGroup: "AB+",
      allergies: false,
      bloodThinners: true,
      pregnant: "NA",
    },
    incident: {
      severity: "HIGH",
      vehicleType: "Truck",
      crashTime: Date.now() - 2 * 60000,
      status: "OPEN",
    },
    emergencyContact: {
      name: "Sunita K.",
      phone: "+91 XXXXX XXXXX",
    },
    hospitalLocation: [20.2961, 85.8245],
    accidentLocation: [20.2989, 85.8290],
    ambulanceLocation: [20.2961, 85.8245],
    claimedBy: null,
  },
];
