import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProjectListPage from "./pages/ProjectListPage";
import ProjectDetailPage from "./pages/ProjectDetailPage";
import ConcreteAdvisorPage from "./pages/ConcreteAdvisorPage";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProjectListPage />} />
        <Route path="/projects/:id" element={<ProjectDetailPage />} />
        <Route path="/concrete-advisor" element={<ConcreteAdvisorPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;