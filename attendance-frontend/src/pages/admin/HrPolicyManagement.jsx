import { useEffect, useRef, useState } from "react";
import { uploadHrPolicy, listHrPolicyDocs, deleteHrPolicyDoc } from "../../api/endpoints";

const statusStyles = {
  ready: "bg-signal-soft text-signal",
  processing: "bg-amber-soft text-amber",
  failed: "bg-clay-soft text-clay",
};

export default function HrPolicyManagement() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const load = () => {
    setLoading(true);
    listHrPolicyDocs()
      .then(setDocs)
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setError("");
    setUploading(true);
    try {
      await uploadHrPolicy(file);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed. Check the backend logs.");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const handleDelete = async (id, filename) => {
    if (!confirm(`Remove "${filename}"? Employees won't be able to ask about it anymore.`)) return;
    await deleteHrPolicyDoc(id);
    load();
  };

  const hasReadyDoc = docs.some((d) => d.status === "ready");

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="font-serif text-lg text-ink">HR Policy Management</h2>
          <p className="text-sm text-ink-muted mt-1">
            Upload once — it's processed and stored permanently. No need to re-upload unless the policy changes.
          </p>
        </div>
        <label className="bg-ink text-white px-4 py-2 rounded-card text-sm hover:bg-ink-light transition-colors cursor-pointer">
          {uploading ? "Processing…" : "+ Upload Policy PDF"}
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleUpload}
            disabled={uploading}
            className="hidden"
          />
        </label>
      </div>

      {error && (
        <div className="mb-4 px-4 py-3 rounded-card bg-clay-soft text-clay text-sm">{error}</div>
      )}

      {!loading && docs.length > 0 && !hasReadyDoc && (
        <div className="mb-4 px-4 py-3 rounded-card bg-amber-soft text-amber text-sm">
          No document is ready yet — the employee chatbot won't have anything to answer from until one finishes processing.
        </div>
      )}

      <div className="bg-surface rounded-card shadow-card overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-canvas text-ink-muted text-xs uppercase tracking-wider">
            <tr>
              <th className="text-left px-5 py-3">Filename</th>
              <th className="text-left px-5 py-3">Chunks</th>
              <th className="text-left px-5 py-3">Uploaded</th>
              <th className="text-left px-5 py-3">Status</th>
              <th className="text-right px-5 py-3">Action</th>
            </tr>
          </thead>
          <tbody>
            {loading && <tr><td colSpan={5} className="px-5 py-4 text-ink-muted">Loading…</td></tr>}
            {!loading && docs.length === 0 && (
              <tr><td colSpan={5} className="px-5 py-4 text-ink-muted">No policy documents uploaded yet.</td></tr>
            )}
            {!loading && docs.map((doc) => (
              <tr key={doc.id} className="border-t border-line">
                <td className="px-5 py-3 text-ink font-medium">{doc.filename}</td>
                <td className="px-5 py-3 font-mono">{doc.chunk_count}</td>
                <td className="px-5 py-3 text-ink-muted font-mono text-xs">
                  {new Date(doc.uploaded_on).toLocaleString("en-IN")}
                </td>
                <td className="px-5 py-3">
                  <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${statusStyles[doc.status]}`}>
                    {doc.status}
                  </span>
                </td>
                <td className="px-5 py-3 text-right">
                  <button
                    onClick={() => handleDelete(doc.id, doc.filename)}
                    className="text-clay text-xs hover:underline"
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
