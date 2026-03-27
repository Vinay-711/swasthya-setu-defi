import React from "react";

/**
 * ASHA Worker Dashboard — home page for ASHA health workers.
 * Shows assigned workers, pending screenings, and recent activity.
 */
export default function AshaDashboard() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">
        🩺 ASHA Worker Dashboard
      </h1>
      <p className="text-gray-500 mb-8">
        View assigned migrant workers, schedule screenings, and track health
        records.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 rounded-xl p-5 border border-blue-100">
          <h3 className="text-sm font-medium text-blue-600">Assigned Workers</h3>
          <p className="text-3xl font-bold text-blue-900 mt-1">24</p>
        </div>
        <div className="bg-amber-50 rounded-xl p-5 border border-amber-100">
          <h3 className="text-sm font-medium text-amber-600">Pending Screenings</h3>
          <p className="text-3xl font-bold text-amber-900 mt-1">8</p>
        </div>
        <div className="bg-green-50 rounded-xl p-5 border border-green-100">
          <h3 className="text-sm font-medium text-green-600">Completed Today</h3>
          <p className="text-3xl font-bold text-green-900 mt-1">5</p>
        </div>
      </div>
    </div>
  );
}
