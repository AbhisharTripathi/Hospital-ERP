// WelcomePage.jsx
import { Link } from "react-router-dom";
import {
  Activity,
  CalendarDays,
  Users,
  ShieldCheck,
  Stethoscope,
  ArrowRight,
} from "lucide-react";

export default function Welcome() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">

      {/* Navbar */}
      <header className="border-b bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 text-white p-2 rounded-xl">
              <Stethoscope size={26} />
            </div>

            <div>
              <h1 className="font-bold text-xl text-slate-800">
                MediCore ERP
              </h1>
              <p className="text-xs text-slate-500">
                Hospital Management System
              </p>
            </div>
          </div>


          {/* Links */}
          <div className="hidden md:flex items-center gap-8 text-sm text-slate-600">
            <a className="hover:text-blue-600">
              Features
            </a>

            <a className="hover:text-blue-600">
              Departments
            </a>

            <a className="hover:text-blue-600">
              Doctors
            </a>

            <a className="hover:text-blue-600">
              Contact
            </a>
          </div>


          {/* Actions */}
          <div className="flex items-center gap-3">

            <Link to="/auth/login" className="
              hidden sm:block
              px-5 py-2
              text-blue-600
              hover:bg-blue-5
              rounded-lg
            ">
              Login
            </Link>

            <Link to="/auth/register" className="btn-primary">
            Register your Hospital
            </Link>

          </div>

        </nav>
      </header>



      {/* Hero */}
      <main className="max-w-7xl mx-auto px-6">

        <section className="
          grid
          md:grid-cols-2
          gap-12
          items-center
          py-20
        ">


          {/* Text */}
          <div>

            <div className="
              inline-flex
              items-center
              gap-2
              bg-blue-100
              text-blue-700
              px-4 py-2
              rounded-full
              text-sm
              mb-6
            ">
              <Activity size={18}/>
              Smart Healthcare Management
            </div>


            <h2 className="
              text-5xl
              font-bold
              leading-tight
              text-slate-900
            ">
              Manage your hospital
              <span className="text-blue-600">
                {" "}smarter
              </span>
            </h2>


            <p className="
              mt-6
              text-lg
              text-slate-600
              max-w-xl
            ">
              A complete Hospital ERP platform that connects
              doctors, patients, departments and administration
              in one powerful system.
            </p>


            <div className="mt-8 flex gap-4">

              <button className="
                flex items-center gap-2
                bg-blue-600
                text-white
                px-6 py-3
                rounded-xl
                hover:bg-blue-700
              ">
                Start Managing
                <ArrowRight size={18}/>
              </button>


              <button className="
                px-6 py-3
                rounded-xl
                border
                border-slate-300
                hover:bg-white
              ">
                Learn More
              </button>

            </div>


            {/* Stats */}
            <div className="
              mt-12
              grid
              grid-cols-3
              gap-6
            ">

              <div>
                <h3 className="text-3xl font-bold text-slate-900">
                  24/7
                </h3>
                <p className="text-sm text-slate-500">
                  Support
                </p>
              </div>


              <div>
                <h3 className="text-3xl font-bold text-slate-900">
                  50+
                </h3>
                <p className="text-sm text-slate-500">
                  Departments
                </p>
              </div>


              <div>
                <h3 className="text-3xl font-bold text-slate-900">
                  99%
                </h3>
                <p className="text-sm text-slate-500">
                  Reliability
                </p>
              </div>

            </div>

          </div>



          {/* Illustration */}
          <div className="
            relative
          ">

            <div className="
              bg-white
              rounded-3xl
              shadow-xl
              p-8
              border
            ">


              <div className="
                grid
                grid-cols-2
                gap-5
              ">

                <Feature
                  icon={<Users/>}
                  title="Patients"
                  value="12,500+"
                />

                <Feature
                  icon={<CalendarDays/>}
                  title="Appointments"
                  value="850/day"
                />


                <Feature
                  icon={<ShieldCheck/>}
                  title="Security"
                  value="Protected"
                />

                <Feature
                  icon={<Activity/>}
                  title="Reports"
                  value="Realtime"
                />

              </div>


              <div className="
                mt-8
                bg-gradient-to-r
                from-blue-600
                to-cyan-500
                rounded-2xl
                p-6
                text-white
              ">

                <h3 className="text-xl font-semibold">
                  Complete Hospital Control
                </h3>

                <p className="mt-2 text-blue-100">
                  OPD, IPD, pharmacy, billing,
                  laboratory and staff management.
                </p>

              </div>

            </div>


            {/* Floating badge */}
            <div className="
              absolute
              -bottom-5
              -left-5
              bg-white
              shadow-lg
              rounded-xl
              px-5
              py-4
            ">

              <p className="text-sm text-slate-500">
                Active Doctors
              </p>

              <p className="text-2xl font-bold text-blue-600">
                250+
              </p>

            </div>

          </div>


        </section>


        {/* Features */}
        <section className="pb-20">

          <h2 className="
            text-3xl
            font-bold
            text-center
            text-slate-900
          ">
            Everything your hospital needs
          </h2>


          <div className="
            mt-10
            grid
            md:grid-cols-3
            gap-6
          ">


            <Card
              icon={<Users/>}
              title="Patient Management"
              text="Complete patient records, history and appointments."
            />


            <Card
              icon={<CalendarDays/>}
              title="Smart Scheduling"
              text="Manage doctors, rooms and appointments easily."
            />


            <Card
              icon={<ShieldCheck/>}
              title="Secure Data"
              text="Protect sensitive medical information."
            />


          </div>

        </section>


      </main>

    </div>
  );
}



function Feature({icon, title, value}) {
  return (
    <div className="
      p-5
      rounded-2xl
      bg-slate-50
    ">
      <div className="text-blue-600">
        {icon}
      </div>

      <p className="mt-3 text-sm text-slate-500">
        {title}
      </p>

      <h3 className="text-xl font-bold">
        {value}
      </h3>
    </div>
  );
}



function Card({icon,title,text}) {
  return (
    <div className="
      bg-white
      p-6
      rounded-2xl
      shadow-sm
      border
      hover:shadow-md
      transition
    ">

      <div className="
        text-blue-600
        mb-4
      ">
        {icon}
      </div>

      <h3 className="
        font-semibold
        text-lg
      ">
        {title}
      </h3>

      <p className="
        mt-2
        text-slate-600
      ">
        {text}
      </p>

    </div>
  );
}