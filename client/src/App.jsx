import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/RuleBased";
import Statistical from "./pages/Statistical";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/statistical" element={<Statistical />} />
      </Routes>
    </Router>
  );
}