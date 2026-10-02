function GlassCard({ children, className = "" }) {
  return (
    <div
      className={`bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.35)] ${className}`}
    >
      {children}
    </div>
  );
}

export default GlassCard;