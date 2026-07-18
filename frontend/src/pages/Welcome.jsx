import { Link } from "react-router-dom";
import {
  Stethoscope,
  Users,
  CalendarDays,
  ShieldCheck,
  ArrowRight,
} from "lucide-react";

export default function WelcomePage() {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Navbar */}
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-blue-600 p-2 text-white">
              <Stethoscope size={24} />
            </div>

            <div>
              <h1 className="text-lg font-bold text-slate-900">
                MediCore ERP
              </h1>

              <p className="text-xs text-slate-500">
                Hospital Management
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <Link
              to="/auth/login"
              className="rounded-lg px-4 py-2 text-slate-700 hover:bg-slate-100"
            >
              Login
            </Link>

            <Link
              to="/auth/register"
              className="rounded-lg bg-blue-600 px-5 py-2 text-white hover:bg-blue-700"
            >
              Register Hospital
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="mx-auto max-w-7xl px-6 py-20">
        <div className="grid items-center gap-16 lg:grid-cols-2">
          {/* Left */}
          <div>
            <span className="rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
              Complete Hospital ERP
            </span>

            <h2 className="mt-6 text-5xl font-bold leading-tight text-slate-900">
              One Platform.
              <br />
              Every Hospital Operation.
            </h2>

            <p className="mt-6 max-w-xl text-lg text-slate-600">
              Manage patients, appointments, billing, pharmacy,
              laboratory and staff from a single secure platform.
            </p>

            <div className="mt-8 flex gap-4">
              <Link
                to="/auth/register"
                className="flex items-center gap-2 rounded-xl bg-blue-600 px-6 py-3 font-medium text-white hover:bg-blue-700"
              >
                Get Started
                <ArrowRight size={18} />
              </Link>

              <Link
                to="/auth/login"
                className="rounded-xl border border-slate-300 px-6 py-3 hover:bg-white"
              >
                Login
              </Link>
            </div>
          </div>

          {/* Right */}
          <div className="rounded-3xl border bg-white p-8 shadow-lg">
            <h3 className="mb-6 text-xl font-semibold">
              Hospital Modules
            </h3>

            <div className="grid gap-4">
              <Module
                icon={<Users size={20} />}
                title="Patient Management"
              />

              <Module
                icon={<CalendarDays size={20} />}
                title="Appointments"
              />

              <Module
                icon={<ShieldCheck size={20} />}
                title="Billing & Security"
              />
            </div>

            <div className="mt-8 rounded-2xl bg-blue-600 p-6 text-white">
              <h4 className="text-lg font-semibold">
                Everything Connected
              </h4>

              <p className="mt-2 text-blue-100">
                Reception • Doctors • Pharmacy • Laboratory •
                Billing • Administration
              </p>
            </div>
          </div>
        </div>

        {/* Features */}
        <section className="mt-24 grid gap-6 md:grid-cols-3">
          <Feature
            title="Fast Registration"
            text="Register patients and staff in seconds."
          />

          <Feature
            title="Centralized Records"
            text="Access patient information from one place."
          />

          <Feature
            title="Secure & Reliable"
            text="Role-based access with secure authentication."
          />
        </section>
      </main>
    </div>
  );
}

function Module({ icon, title }) {
  return (
    <div className="flex items-center gap-4 rounded-xl bg-slate-50 p-4">
      <div className="rounded-lg bg-blue-100 p-3 text-blue-600">
        {icon}
      </div>

      <span className="font-medium text-slate-800">
        {title}
      </span>
    </div>
  );
}

function Feature({ title, text }) {
  return (
    <div className="rounded-2xl border bg-white p-6">
      <h3 className="text-lg font-semibold">{title}</h3>

      <p className="mt-2 text-slate-600">
        {text}
      </p>
    </div>
  );
}