import { Calendar, AlertCircle, FileText } from 'lucide-react';
import { useState, useEffect } from 'react';

export function RightSidebar() {
  const [currentDate, setCurrentDate] = useState(new Date());

  // Calendar logic
  const currentMonthName = currentDate.toLocaleString('default', { month: 'long' });
  const currentYear = currentDate.getFullYear();
  const daysInMonth = new Date(currentYear, currentDate.getMonth() + 1, 0).getDate();
  const today = currentDate.getDate();

  // Recent scans logic (live dates)
  const formatDate = (date: Date) => date.toLocaleString('default', { month: 'short', day: 'numeric' });
  
  const getRecentDate = (daysAgo: number) => {
    const d = new Date();
    d.setDate(d.getDate() - daysAgo);
    return formatDate(d);
  };

  return (
    <div className="w-80 space-y-4 pb-6">
      <div className="bg-white/70 backdrop-blur-lg rounded-2xl p-5 shadow-xl border border-teal-100">
        <div className="flex items-center gap-2 mb-4">
          <Calendar className="w-5 h-5 text-teal-600" />
          <h3 className="text-teal-900">Calendar</h3>
        </div>
        <div className="bg-teal-50/80 rounded-xl p-4 border border-teal-200">
          <div className="text-center mb-4">
            <p className="text-teal-900">{currentMonthName} {currentYear}</p>
          </div>
          <div className="grid grid-cols-7 gap-1 text-center text-sm">
            {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((day, index) => (
              <div key={`day-label-${index}`} className="text-teal-600 py-1">
                {day}
              </div>
            ))}
            {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((day) => (
              <button
                key={`day-${day}`}
                className={`py-1 rounded-lg hover:bg-teal-200 transition-colors ${
                  day === today ? 'bg-teal-500 text-white' : 'text-teal-700'
                }`}
              >
                {day}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white/70 backdrop-blur-lg rounded-2xl p-5 shadow-xl border border-teal-100">
        <h3 className="text-teal-900 mb-4">AI Model Accuracy</h3>

        <div className="flex items-center justify-center mb-4">
          <div className="relative w-40 h-40">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="80"
                cy="80"
                r="70"
                stroke="#d1f0ed"
                strokeWidth="12"
                fill="none"
              />
              <circle
                cx="80"
                cy="80"
                r="70"
                stroke="#14b8a6"
                strokeWidth="12"
                fill="none"
                strokeDasharray={`${2 * Math.PI * 70}`}
                strokeDashoffset={`${2 * Math.PI * 70 * (1 - 0.99)}`}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center flex-col">
              <p className="text-4xl text-teal-900">99%</p>
              <p className="text-teal-600 text-sm">Accuracy</p>
            </div>
          </div>
        </div>

        <div className="bg-teal-50/80 rounded-xl p-4 border border-teal-200">
          <p className="text-teal-900 mb-1">Glioma Detection</p>
          <p className="text-teal-600 text-sm">924 scans analyzed</p>
        </div>
      </div>

      <div className="bg-white/70 backdrop-blur-lg rounded-2xl p-5 shadow-xl border border-teal-100">
        <div className="flex items-center gap-2 mb-3">
          <AlertCircle className="w-5 h-5 text-teal-600" />
          <h3 className="text-teal-900">MRI Scan Guidelines</h3>
        </div>

        <ul className="space-y-2">
          <li className="flex items-start gap-2">
            <div className="w-1.5 h-1.5 bg-teal-500 rounded-full mt-2"></div>
            <p className="text-teal-700 text-sm">Ensure no metal objects are present</p>
          </li>
          <li className="flex items-start gap-2">
            <div className="w-1.5 h-1.5 bg-teal-500 rounded-full mt-2"></div>
            <p className="text-teal-700 text-sm">Stay still during the scan</p>
          </li>
          <li className="flex items-start gap-2">
            <div className="w-1.5 h-1.5 bg-teal-500 rounded-full mt-2"></div>
            <p className="text-teal-700 text-sm">Inform technician of any implants</p>
          </li>
          <li className="flex items-start gap-2">
            <div className="w-1.5 h-1.5 bg-teal-500 rounded-full mt-2"></div>
            <p className="text-teal-700 text-sm">Follow fasting instructions if required</p>
          </li>
        </ul>
      </div>

      <div className="bg-white/70 backdrop-blur-lg rounded-2xl p-5 shadow-xl border border-teal-100">
        <div className="flex items-center gap-2 mb-3">
          <FileText className="w-5 h-5 text-teal-600" />
          <h3 className="text-teal-900">Recent Scans</h3>
        </div>

        <div className="space-y-2">
          {[
            { id: '#217890', type: 'Glioma', date: getRecentDate(0) },
            { id: '#215623', type: 'No Tumor', date: getRecentDate(2) },
            { id: '#213451', type: 'Meningioma', date: getRecentDate(5) }
          ].map((scan) => (
            <div key={scan.id} className="flex items-center justify-between p-3 bg-teal-50/80 rounded-xl border border-teal-200 hover:bg-teal-50 transition-colors cursor-pointer">
              <div>
                <p className="text-teal-900 font-mono text-sm">{scan.id}</p>
                <p className="text-teal-600 text-xs">{scan.type}</p>
              </div>
              <p className="text-teal-500 text-xs">{scan.date}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
