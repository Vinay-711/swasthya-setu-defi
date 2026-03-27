import { Link, Outlet, useLocation } from 'react-router-dom';
import {
  Smartphone, HeartPulse, Stethoscope, Building2,
  Route, Cpu, LayoutGrid
} from 'lucide-react';

const portalLinks = [
  { to: '/',             label: 'Mobile Home',   icon: Smartphone,  color: '#E5681A' },
  { to: '/asha',         label: 'ASHA',          icon: HeartPulse,   color: '#2D8C4E' },
  { to: '/doctor',       label: 'Doctor',        icon: Stethoscope,  color: '#7C3AED' },
  { to: '/employer',     label: 'Employer',      icon: Building2,    color: '#2563EB' },
  { to: '/journey',      label: 'Journey',       icon: Route,        color: '#0D9488' },
  { to: '/architecture', label: 'Architecture',  icon: LayoutGrid,   color: '#6B7280' },
  { to: '/tech-stack',   label: 'Tech Stack',    icon: Cpu,          color: '#D97706' },
];

export default function PortalNav() {
  const { pathname } = useLocation();

  const isActive = (to) => {
    if (to === '/') return pathname === '/';
    return pathname.startsWith(to);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Navigation Bar */}
      <header className="bg-gray-900 px-4 py-2 flex items-center gap-1 overflow-x-auto shrink-0">
        <span className="text-white font-bold text-base mr-4 shrink-0">SwasthyaSetu</span>

        <nav className="flex items-center gap-1">
          {portalLinks.map((link) => {
            const Icon = link.icon;
            const active = isActive(link.to);
            return (
              <Link
                key={link.to}
                to={link.to}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium transition-all duration-200 shrink-0 no-underline"
                style={{
                  backgroundColor: active ? link.color : 'transparent',
                  color: active ? '#fff' : '#9ca3af',
                  borderBottom: active ? `2px solid ${link.color}` : '2px solid transparent',
                }}
              >
                <Icon size={16} />
                <span className="hidden sm:inline">{link.label}</span>
              </Link>
            );
          })}
        </nav>
      </header>

      {/* Page Content */}
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
}
