import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import GlassCard from "../components/GlassCard";

function ConcreteAdvisorPage() {
  const [mix, setMix] = useState({
    cement_kg: "",
    blast_furnace_slag_kg: "",
    fly_ash_kg: "",
    water_kg: "",
    superplasticizer_kg: "",
    coarse_aggregate_kg: "",
    fine_aggregate_kg: "",
    age_days: "28",
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setMix({ ...mix, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post("/concrete/predict-strength", {
        cement_kg: parseFloat(mix.cement_kg),
        blast_furnace_slag_kg: parseFloat(mix.blast_furnace_slag_kg) || 0,
        fly_ash_kg: parseFloat(mix.fly_ash_kg) || 0,
        water_kg: parseFloat(mix.water_kg),
        superplasticizer_kg: parseFloat(mix.superplasticizer_kg) || 0,
        coarse_aggregate_kg: parseFloat(mix.coarse_aggregate_kg),
        fine_aggregate_kg: parseFloat(mix.fine_aggregate_kg),
        age_days: parseInt(mix.age_days) || 28,
      });
      setResult(res.data);
    } finally {
      setLoading(false);
    }
  };

  const inputClass =
    "p-3 rounded-xl bg-white/5 border border-white/10 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition";

  return (
    <div className="min-h-screen text-white p-8 max-w-4xl mx-auto">
      <Link to="/" className="text-slate-400 hover:text-white text-sm mb-4 inline-block">← All Projects</Link>
      <h1 className="text-3xl font-semibold mb-1">Concrete Mix Advisor 🧱</h1>
      <p className="text-slate-400 mb-8">
        Predict 28-day compressive strength from a proposed concrete mix design.
      </p>

      <GlassCard className="p-6 mb-6">
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <input name="cement_kg" value={mix.cement_kg} onChange={handleChange}
            placeholder="Cement (kg/m³)" type="number" required className={inputClass} />
          <input name="water_kg" value={mix.water_kg} onChange={handleChange}
            placeholder="Water (kg/m³)" type="number" required className={inputClass} />
          <input name="coarse_aggregate_kg" value={mix.coarse_aggregate_kg} onChange={handleChange}
            placeholder="Coarse Aggregate (kg/m³)" type="number" required className={inputClass} />
          <input name="fine_aggregate_kg" value={mix.fine_aggregate_kg} onChange={handleChange}
            placeholder="Fine Aggregate (kg/m³)" type="number" required className={inputClass} />
          <input name="blast_furnace_slag_kg" value={mix.blast_furnace_slag_kg} onChange={handleChange}
            placeholder="Blast Furnace Slag (kg/m³) — optional" type="number" className={inputClass} />
          <input name="fly_ash_kg" value={mix.fly_ash_kg} onChange={handleChange}
            placeholder="Fly Ash (kg/m³) — optional" type="number" className={inputClass} />
          <input name="superplasticizer_kg" value={mix.superplasticizer_kg} onChange={handleChange}
            placeholder="Superplasticizer (kg/m³) — optional" type="number" className={inputClass} />
          <input name="age_days" value={mix.age_days} onChange={handleChange}
            placeholder="Age at testing (days)" type="number" className={inputClass} />

          <button type="submit" disabled={loading}
            className="col-span-2 bg-blue-600 hover:bg-blue-500 active:scale-[0.98] transition rounded-xl p-3 font-semibold shadow-lg shadow-blue-900/30 disabled:opacity-50">
            {loading ? "Predicting..." : "Predict Strength"}
          </button>
        </form>
      </GlassCard>

      {result && (
        <GlassCard className="p-6">
          <h3 className="font-semibold mb-4">Prediction Result</h3>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <div className="text-slate-400 text-sm">Predicted Strength</div>
              <div className="text-2xl font-semibold text-emerald-400">{result.predicted_strength_mpa} MPa</div>
            </div>
            <div>
              <div className="text-slate-400 text-sm">Nearest Grade</div>
              <div className="text-2xl font-semibold text-blue-400">{result.nearest_grade}</div>
            </div>
            <div>
              <div className="text-slate-400 text-sm">Water/Cement Ratio</div>
              <div className="text-2xl font-semibold">{result.water_cement_ratio}</div>
            </div>
          </div>
          <p className="text-xs text-slate-500 mt-4">
            Prediction based on a Random Forest model trained on the UCI Concrete Compressive Strength dataset. For reference only — final mix approval should follow IS 10262 mix design guidelines and site trial mixes.
          </p>
        </GlassCard>
      )}
    </div>
  );
}

export default ConcreteAdvisorPage;