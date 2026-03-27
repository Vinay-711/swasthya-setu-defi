import React from "react";

/**
 * Worker Self-Service Portal — for migrant workers themselves.
 * Shows health records, SwasthyaID QR, upcoming appointments.
 */
export default function WorkerPortal() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">
        👷 My Health Portal
      </h1>
      <p className="text-gray-500 mb-8">
        View your health records, SwasthyaID, and upcoming screenings.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-blue-50 rounded-xl p-5 border border-blue-100">
          <h3 className="text-sm font-medium text-blue-600">SwasthyaID</h3>
          <p className="text-xl font-bold text-blue-900 mt-1 font-mono">
            SID-A3F8K2M1
          </p>
        </div>
        <div className="bg-green-50 rounded-xl p-5 border border-green-100">
          <h3 className="text-sm font-medium text-green-600">Next Checkup</h3>
          <p className="text-xl font-bold text-green-900 mt-1">April 15, 2025</p>
        </div>
      </div>
    </div>
  );
}
