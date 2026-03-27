import React from "react";

/**
 * Employer Dashboard — for factory/site owners who employ migrant workers.
 * Shows compliance, PPE tracking, and workforce health summary.
 */
export default function EmployerDashboard() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">
        🏭 Employer Dashboard
      </h1>
      <p className="text-gray-500 mb-8">
        Monitor workforce health, track compliance, and manage PPE distribution.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-indigo-50 rounded-xl p-5 border border-indigo-100">
          <h3 className="text-sm font-medium text-indigo-600">Total Workers</h3>
          <p className="text-3xl font-bold text-indigo-900 mt-1">156</p>
        </div>
        <div className="bg-orange-50 rounded-xl p-5 border border-orange-100">
          <h3 className="text-sm font-medium text-orange-600">PPE Compliance</h3>
          <p className="text-3xl font-bold text-orange-900 mt-1">78%</p>
        </div>
        <div className="bg-green-50 rounded-xl p-5 border border-green-100">
          <h3 className="text-sm font-medium text-green-600">Health Score</h3>
          <p className="text-3xl font-bold text-green-900 mt-1">B+</p>
        </div>
      </div>
    </div>
  );
}
