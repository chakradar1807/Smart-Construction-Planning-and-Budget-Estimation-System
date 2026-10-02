import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import GlassCard from "../components/GlassCard";

function ProjectListPage() {
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({
  project_name: "",
  location: "",
  total_land_area: "",
  construction_area: "",
  open_area: "",
  number_of_floors: "",
  basement: false,
  parking_cars: "",
});

  const fetchProjects = async () => {
    const res = await api.get("/projects/");
    setProjects(res.data);
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({ ...form, [name]: type === "checkbox" ? checked : value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post("/projects/", {
  ...form,
  total_land_area: parseFloat(form.total_land_area),
  construction_area: parseFloat(form.construction_area),
  open_area: form.open_area ? parseFloat(form.open_area) : null,
  number_of_floors: form.number_of_floors ? parseInt(form.number_of_floors) : 1,
  parking_cars: form.parking_cars ? parseInt(form.parking_cars) : 0,
});
    fetchProjects();
    setForm({
      project_name: "",
      location: "",
      total_land_area: "",
      construction_area: "",
      open_area: "",
      number_of_floors: "",
      basement: false,
      parking_cars: "",
    });
  };

  const deleteProject = async (e, projectId) => {
  e.preventDefault();
  e.stopPropagation();
  if (window.confirm("Delete this project? This cannot be undone.")) {
    await api.delete(`/projects/${projectId}`);
    fetchProjects();
  }
};
  const inputClass =
    "p-3 rounded-xl bg-white/5 border border-white/10 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition";

  return (
    <div className="min-h-screen text-white p-8 max-w-5xl mx-auto">
      <div className="flex justify-between items-start mb-8">
  <div>
    <h1 className="text-4xl font-semibold mb-1 tracking-tight">
      Smart Construction System 🏗️
    </h1>
    <p className="text-slate-400">Plan, estimate, and supervise your build.</p>
  </div>
  <Link to="/concrete-advisor"
    className="text-sm px-4 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition">
    🧱 Concrete Mix Advisor
  </Link>
</div>

      <GlassCard className="p-6 mb-10">
        <h2 className="text-lg font-semibold mb-4">Create a New Project</h2>
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <input name="project_name" value={form.project_name} onChange={handleChange}
            placeholder="Project Name" required className={inputClass} />
          <input name="location" value={form.location} onChange={handleChange}
            placeholder="Location" className={inputClass} />
          <input name="total_land_area" value={form.total_land_area} onChange={handleChange}
            placeholder="Total Land Area (sq.ft)" type="number" required className={inputClass} />
          <input name="construction_area" value={form.construction_area} onChange={handleChange}
            placeholder="Construction Area (sq.ft)" type="number" required className={inputClass} />
          <input name="open_area" value={form.open_area} onChange={handleChange}
            placeholder="Open Area (sq.ft)" type="number" className={inputClass} />
          <input name="number_of_floors" value={form.number_of_floors} onChange={handleChange}
            placeholder="Number of Floors" type="number" className={inputClass} />
          <input name="parking_cars" value={form.parking_cars} onChange={handleChange}
            placeholder="Parking (cars)" type="number" className={inputClass} />
          <label className="flex items-center gap-2 text-slate-300">
            <input name="basement" checked={form.basement} onChange={handleChange} type="checkbox" />
            Basement
          </label>
          <button type="submit"
            className="col-span-2 bg-blue-600 hover:bg-blue-500 active:scale-[0.98] transition rounded-xl p-3 font-semibold shadow-lg shadow-blue-900/30">
            Create Project
          </button>
        </form>
      </GlassCard>

      <h2 className="text-xl font-semibold mb-4">Your Projects</h2>
      <div className="grid gap-4">
        {projects.map((p) => (
  <Link key={p.id} to={`/projects/${p.id}`}>
    <GlassCard className="p-5 hover:bg-white/10 active:scale-[0.99] transition cursor-pointer relative group">
      <button
        onClick={(e) => deleteProject(e, p.id)}
        className="absolute top-4 right-4 text-xs px-2 py-1 rounded-lg bg-red-600/20 hover:bg-red-600/40 text-red-300 transition opacity-0 group-hover:opacity-100"
      >
        Delete
      </button>
      <div className="font-semibold text-lg">{p.project_name} <span className="text-slate-400 font-normal">({p.location})</span></div>
      <div className="text-sm text-slate-400 mt-1">
        Land: {p.total_land_area} sq.ft · Built-up: {p.construction_area} sq.ft ·
        Floors: {p.number_of_floors} · Basement: {p.basement ? "Yes" : "No"} ·
        Parking: {p.parking_cars}
      </div>
    </GlassCard>
  </Link>
))}
      </div>
    </div>
  );


}

export default ProjectListPage;