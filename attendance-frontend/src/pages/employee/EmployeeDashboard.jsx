// import { useEffect, useState } from "react";
// import { checkIn, checkOut, myAttendance } from "../../api/endpoints";
// import PresenceRibbon from "../../components/PresenceRibbon";
// import { useAuth } from "../../context/AuthContext";

// export default function EmployeeDashboard() {
//   const { user } = useAuth();
//   const [records, setRecords] = useState([]);
//   const [message, setMessage] = useState("");
//   const [loading, setLoading] = useState(true);

//   const load = () => {
//     myAttendance()
//       .then(setRecords)
//       .finally(() => setLoading(false));
//   };

//   useEffect(load, []);

//   const isPastCutoff = () => {
//   const now = new Date();
//   return now.getHours() >= 10; // 10:00 AM cutoff, matches backend
// };

//   const today = new Date().toISOString().slice(0, 10);
//   const todayRecord = records.find((r) => r.date === today);

//   const handleCheckIn = async () => {
//     setMessage("");
//     try {
//       await checkIn();
//       setMessage("Checked in successfully.");
//       load();
//     } catch (err) {
//       setMessage(err.response?.data?.detail || "Could not check in.");
//     }
//   };

//   const handleCheckOut = async () => {
//     setMessage("");
//     try {
//       await checkOut();
//       setMessage("Checked out successfully.");
//       load();
//     } catch (err) {
//       setMessage(err.response?.data?.detail || "Could not check out.");
//     }
//   };

//   return (
//     <div>
//       <div className="bg-surface rounded-card shadow-card p-6 mb-6 flex items-center justify-between">
//         <div>
//           <h2 className="font-serif text-lg text-ink">Welcome back, {user?.name}</h2>
//           <p className="text-sm text-ink-muted mt-1">
//             {todayRecord?.check_in_time
//               ? `Checked in at ${new Date(todayRecord.check_in_time).toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" })}`
//               : "You haven't checked in today."}
//           </p>
//         </div>
//         <div className="flex gap-3">
//           <button
//             onClick={handleCheckIn}
//             disabled={!!todayRecord?.check_in_time}
//             className="bg-signal text-white px-5 py-2.5 rounded-card text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
//           >
//             Check in
//           </button>
//           <button
//             onClick={handleCheckOut}
//             disabled={!todayRecord?.check_in_time || !!todayRecord?.check_out_time}
//             className="bg-ink text-white px-5 py-2.5 rounded-card text-sm font-medium hover:bg-ink-light transition-colors disabled:opacity-40"
//           >
//             Check out
//           </button>
//         </div>
//       </div>

//       {message && <p className="text-sm text-ink-muted mb-6">{message}</p>}

//       <div className="bg-surface rounded-card shadow-card p-6">
//         <h3 className="font-serif text-lg text-ink mb-4">Your Recent Attendance</h3>
//         {loading && <p className="text-sm text-ink-muted">Loading…</p>}
//         {!loading && records.length === 0 && (
//           <p className="text-sm text-ink-muted">No attendance history yet.</p>
//         )}
//         {!loading &&
//           records
//             .slice(0, 10)
//             .map((r) => (
//               <PresenceRibbon
//                 key={r.id}
//                 name={r.date}
//                 checkIn={r.check_in_time}
//                 checkOut={r.check_out_time}
//                 status={r.status}
//               />
//             ))}
//       </div>
//     </div>
//   );
// }



import { useEffect, useState } from "react";
import { checkIn, checkOut, myAttendance } from "../../api/endpoints";
import PresenceRibbon from "../../components/PresenceRibbon";
import { useAuth } from "../../context/AuthContext";

const CHECK_IN_CUTOFF_HOUR = 10; // 10:00 AM - must match backend CHECK_IN_CUTOFF

export default function EmployeeDashboard() {
  const { user } = useAuth();
  const [records, setRecords] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  const load = () => {
    myAttendance()
      .then(setRecords)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  const today = new Date().toISOString().slice(0, 10);
  const todayRecord = records.find((r) => r.date === today);

  const isPastCutoff = () => new Date().getHours() >= CHECK_IN_CUTOFF_HOUR;

  const handleCheckIn = async () => {
    setMessage("");
    try {
      await checkIn();
      setMessage("Checked in successfully.");
      load();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Could not check in.");
    }
  };

  const handleCheckOut = async () => {
    setMessage("");
    try {
      await checkOut();
      setMessage("Checked out successfully.");
      load();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Could not check out.");
    }
  };

  const alreadyCheckedIn = !!todayRecord?.check_in_time;
  const checkInDisabled = alreadyCheckedIn || isPastCutoff();

  return (
    <div>
      <div className="bg-surface dark:bg-night-surface rounded-card shadow-card p-6 mb-6 flex items-center justify-between transition-colors">
        <div>
          <h2 className="font-serif text-lg text-ink dark:text-night-text">Welcome back, {user?.name}</h2>
          <p className="text-sm text-ink-muted dark:text-night-muted mt-1">
            {alreadyCheckedIn
              ? `Checked in at ${new Date(todayRecord.check_in_time).toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" })}`
              : isPastCutoff()
              ? "Check-in window closed for today (cutoff: 10:00 AM). Contact your admin."
              : "You haven't checked in today."}
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleCheckIn}
            disabled={checkInDisabled}
            className="bg-signal text-white px-5 py-2.5 rounded-card text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
          >
            Check in
          </button>
          <button
            onClick={handleCheckOut}
            disabled={!todayRecord?.check_in_time || !!todayRecord?.check_out_time}
            className="bg-ink text-white px-5 py-2.5 rounded-card text-sm font-medium hover:bg-ink-light transition-colors disabled:opacity-40"
          >
            Check out
          </button>
        </div>
      </div>

      {message && <p className="text-sm text-ink-muted dark:text-night-muted mb-6">{message}</p>}

      <div className="bg-surface dark:bg-night-surface rounded-card shadow-card p-6 transition-colors">
        <h3 className="font-serif text-lg text-ink dark:text-night-text mb-4">Your Recent Attendance</h3>
        {loading && <p className="text-sm text-ink-muted dark:text-night-muted">Loading…</p>}
        {!loading && records.length === 0 && (
          <p className="text-sm text-ink-muted dark:text-night-muted">No attendance history yet.</p>
        )}
        {!loading &&
          records
            .slice(0, 10)
            .map((r) => (
              <PresenceRibbon
                key={r.id}
                name={r.date}
                checkIn={r.check_in_time}
                checkOut={r.check_out_time}
                status={r.status}
              />
            ))}
      </div>
    </div>
  );
}