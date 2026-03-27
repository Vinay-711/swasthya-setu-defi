import React from "react";

/**
 * Doctor Dashboard — for registered medical professionals.
 * Shows patient queue, risk alerts, and prescription history.
 */
export default function DoctorDashboard() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">
        👨‍⚕️ Doctor Dashboard
      </h1>
      <p className="text-gray-500 mb-8">
        Review patient records, submit diagnoses, and manage referrals.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-purple-50 rounded-xl p-5 border border-purple-100">
          <h3 className="text-sm font-medium text-purple-600">Patient Queue</h3>
          <p className="text-3xl font-bold text-purple-900 mt-1">12</p>
        </div>
        <div className="bg-red-50 rounded-xl p-5 border border-red-100">
          <h3 className="text-sm font-medium text-red-600">High-Risk Alerts</h3>
          <p className="text-3xl font-bold text-red-900 mt-1">3</p>
        </div>
        <div className="bg-teal-50 rounded-xl p-5 border border-teal-100">
          <h3 className="text-sm font-medium text-teal-600">Prescriptions Today</h3>
          <p className="text-3xl font-bold text-teal-900 mt-1">9</p>
        </div>
      </div>
    </div>
  );
}
