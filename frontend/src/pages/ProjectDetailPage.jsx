import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api";
import GlassCard from "../components/GlassCard";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis } from "recharts";

const CATEGORIES = ["Economy", "Standard", "Premium", "Luxury"];
const TABS = ["Planning", "Risk & Safety", "Construction"];

function ProjectDetailPage() {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [activeTab, setActiveTab] = useState("Planning");
  const [quantities, setQuantities] = useState(null);
  const [cost, setCost] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [risks, setRisks] = useState(null);
  const [stages, setStages] = useState([]);
  const [activeStageId, setActiveStageId] = useState(null);

  useEffect(() => {
    api.get(`/projects/${id}`).then((res) => setProject(res.data));
    api.get(`/projects/${id}/quantities`).then((res) => setQuantities(res.data));
  }, [id]);

  useEffect(() => {
    if (activeTab === "Construction") {
      fetchStages();
    }
  }, [activeTab, id]);

  const fetchCost = async (category) => {
    const res = await api.get(`/projects/${id}/cost`, { params: { category } });
    setCost(res.data);
  };

  const fetchPrediction = async (category) => {
    const res = await api.get(`/projects/${id}/predict`, { params: { category } });
    setPrediction(res.data);
  };

  const fetchStages = async () => {
    const res = await api.get(`/projects/${id}/stages`);
    setStages(res.data);
  };

  const startStage = async (stageId) => {
    await api.patch(`/projects/${id}/stages/${stageId}/start`);
    fetchStages();
  };

  const updateInspection = async (inspectionId, status) => {
    try {
      await api.patch(`/projects/inspections/${inspectionId}`, { status });
      fetchStages();
    } catch (err) {
      console.error(err);
      alert("Failed to update inspection status.");
    }
  };

  const uploadPhoto = async (inspectionId, file) => {
    try {
      const formData = new FormData();
      formData.append("file", file);
      await api.post(`/projects/inspections/${inspectionId}/photos`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      fetchStages();
    } catch (err) {
      console.error(err);
      alert("Failed to upload photo.");
    }
  };

  const fetchRisks = async () => {
    const res = await api.get(`/projects/${id}/risks`);
    setRisks(res.data);
  };

  if (!project) return <div className="min-h-screen text-white p-8">Loading...</div>;

  const inputClass =
    "px-4 py-2 rounded-xl text-sm font-medium transition";

  return (
    <div className="min-h-screen text-white p-8 max-w-5xl mx-auto">
      <Link to="/" className="text-slate-400 hover:text-white text-sm mb-4 inline-block">← All Projects</Link>
      <h1 className="text-3xl font-semibold mb-1">{project.project_name}</h1>
      <p className="text-slate-400 mb-6">{project.location}</p>

      <GlassCard className="p-4 mb-6 flex gap-3 flex-wrap">
        {quantities && (
          <>
            <span className="text-sm text-slate-300">Built-up: {quantities.total_built_up_area} sq.ft</span>
            <span className="text-sm text-slate-500">·</span>
            <span className="text-sm text-slate-300">Floors: {project.number_of_floors}</span>
            <span className="text-sm text-slate-500">·</span>
            <span className="text-sm text-slate-300">Basement: {project.basement ? "Yes" : "No"}</span>
          </>
        )}
      </GlassCard>

      <div className="flex gap-2 mb-6">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`${inputClass} ${
              activeTab === tab
                ? "bg-white/15 text-white shadow-inner"
                : "text-slate-400 hover:text-white hover:bg-white/5"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {activeTab === "Planning" && (
        <div className="space-y-6">
          <GlassCard className="p-6">
            <h3 className="font-semibold mb-4">Material Quantities</h3>
            {quantities && (
              <div className="grid grid-cols-2 gap-3 text-sm text-slate-300">
                <div>Cement: {quantities.cement_bags} bags</div>
                <div>Steel: {quantities.steel_kg} kg</div>
                <div>Sand: {quantities.sand_cft} cu.ft</div>
                <div>Aggregate: {quantities.aggregate_cft} cu.ft</div>
                <div>Bricks: {quantities.bricks_units} units</div>
              </div>
            )}
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="font-semibold mb-4">Cost Estimate</h3>
            <div className="flex gap-2 mb-4 flex-wrap">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat}
                  onClick={() => fetchCost(cat)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium transition ${
                    cost?.category === cat
                      ? "bg-amber-500 text-slate-900"
                      : "bg-white/5 text-slate-300 hover:bg-white/10"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
            {cost && (
  <div className="mt-4 h-48">
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={[
            { name: "Material", value: cost.material_cost },
            { name: "Labour", value: cost.labour_cost },
            { name: "Contingency", value: cost.contingency },
            { name: "Other", value: cost.other_cost },
          ]}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={70}
          label={(entry) => entry.name}
        >
          {["#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6"].map((color, i) => (
            <Cell key={i} fill={color} />
          ))}
        </Pie>
        <Tooltip
          formatter={(value) => `₹${value.toLocaleString()}`}
          contentStyle={{ backgroundColor: "#1e293b", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "8px" }}
        />
      </PieChart>
    </ResponsiveContainer>
  </div>
)}
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="font-semibold mb-4">ML Prediction</h3>
            <button
              onClick={() => fetchPrediction(cost?.category || "Standard")}
              className="px-4 py-1.5 rounded-full text-sm font-medium bg-purple-600 hover:bg-purple-500 transition mb-4"
            >
              Predict ({cost?.category || "Standard"})
            </button>
            {prediction && (
              <div className="grid grid-cols-2 gap-3 text-sm text-slate-300">
                <div className="font-semibold text-purple-400 text-base">
                  ₹{prediction.predicted_cost.toLocaleString()}
                </div>
                <div>{prediction.predicted_duration_weeks} weeks</div>
                <div className="col-span-2 text-slate-400">
                  Range: ₹{prediction.cost_range_low.toLocaleString()} – ₹{prediction.cost_range_high.toLocaleString()}
                </div>
              </div>
            )}
          </GlassCard>
        </div>
      )}

      {activeTab === "Risk & Safety" && (
        <GlassCard className="p-6">
          <button
            onClick={fetchRisks}
            className="px-4 py-1.5 rounded-full text-sm font-medium bg-rose-600 hover:bg-rose-500 transition mb-4"
          >
            Run Risk Check
          </button>
          {risks && (
            <div className="text-sm">
              <div className="font-semibold mb-3">
                Overall Risk:{" "}
                <span className={
                  risks.overall_risk === "High" ? "text-red-400" :
                  risks.overall_risk === "Medium" ? "text-orange-400" :
                  risks.overall_risk === "Low-Medium" ? "text-yellow-400" : "text-emerald-400"
                }>
                  {risks.overall_risk}
                </span>
              </div>
              <ul className="space-y-2">
                {risks.warnings.map((w, i) => (
                  <li key={i} className="text-slate-300">
                    <span className={
                      w.level === "critical" ? "text-red-400 font-semibold" :
                      w.level === "warning" ? "text-yellow-400 font-semibold" : "text-blue-400 font-semibold"
                    }>[{w.category}]</span> {w.message}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </GlassCard>
      )}

      {activeTab === "Construction" && (
        <div className="space-y-4">
          {/* Stage tracker bar */}
          <GlassCard className="p-4 flex gap-2 flex-wrap">
            {stages.map((stage) => (
              <button
                key={stage.id}
                onClick={() => setActiveStageId(stage.id)}
                className={`px-4 py-2 rounded-xl text-sm font-medium capitalize transition ${
                  activeStageId === stage.id
                    ? "bg-blue-600 text-white"
                    : stage.status === "completed"
                    ? "bg-emerald-600/30 text-emerald-300"
                    : stage.status === "in_progress"
                    ? "bg-amber-600/30 text-amber-300"
                    : "bg-white/5 text-slate-400 hover:bg-white/10"
                }`}
              >
                {stage.stage_name} {stage.status === "completed" && "✓"}
              </button>
            ))}
          </GlassCard>

          {/* Selected stage detail */}
          {stages
            .filter((s) => s.id === activeStageId)
            .map((stage) => (
              <GlassCard key={stage.id} className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-semibold capitalize">{stage.stage_name} Stage</h3>
                  {stage.status === "not_started" && (
                    <button
                      onClick={() => startStage(stage.id)}
                      className="px-4 py-1.5 rounded-full text-sm font-medium bg-blue-600 hover:bg-blue-500 transition"
                    >
                      Start Stage
                    </button>
                  )}
                </div>

                {stage.inspections.length === 0 && stage.status !== "not_started" && (
                  <p className="text-slate-400 text-sm">No checklist items for this stage yet.</p>
                )}

                <div className="space-y-3">
                  {stage.inspections.map((item) => (
                    <div key={item.id} className="bg-white/5 rounded-xl p-4">
                      <div className="flex justify-between items-start gap-3">
                        <div>
                          <div className="font-medium text-sm">{item.title}</div>
                          <div className="text-xs text-slate-500 mt-0.5 capitalize">{item.category.replace("_", " ")}</div>
                        </div>
                        <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                          item.status === "pass" ? "bg-emerald-600/30 text-emerald-300" :
                          item.status === "fail" ? "bg-red-600/30 text-red-300" :
                          item.status === "na" ? "bg-slate-600/30 text-slate-300" :
                          "bg-amber-600/30 text-amber-300"
                        }`}>
                          {item.status}
                        </span>
                      </div>

                      <div className="flex gap-2 mt-3 flex-wrap items-center">
                        <button onClick={() => updateInspection(item.id, "pass")}
                          className="text-xs px-3 py-1 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 transition">
                          Pass
                        </button>
                        <button onClick={() => updateInspection(item.id, "fail")}
                          className="text-xs px-3 py-1 rounded-lg bg-red-600/20 hover:bg-red-600/40 text-red-300 transition">
                          Fail
                        </button>
                        <button onClick={() => updateInspection(item.id, "na")}
                          className="text-xs px-3 py-1 rounded-lg bg-slate-600/20 hover:bg-slate-600/40 text-slate-300 transition">
                          N/A
                        </button>
                        <label className="text-xs px-3 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 transition cursor-pointer">
                          📷 Photo
                          <input type="file" accept="image/*" className="hidden"
                            onChange={(e) => e.target.files[0] && uploadPhoto(item.id, e.target.files[0])} />
                        </label>
                      </div>

                      {item.photos.length > 0 && (
                        <div className="flex gap-2 flex-wrap mt-2">
                          {item.photos.map((photo) => (
                            <a
                              key={photo.id}
                              href={`http://127.0.0.1:8000/${photo.file_path}`}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              <img
                                src={`http://127.0.0.1:8000/${photo.file_path}`}
                                alt="inspection"
                                className="w-16 h-16 object-cover rounded-lg border border-white/10 hover:opacity-80 transition"
                              />
                            </a>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </GlassCard>
            ))}
        </div>
      )}
    </div>
  );
}

export default ProjectDetailPage;
