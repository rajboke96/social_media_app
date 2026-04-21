import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';

// Simple Page Components
const Home = () => <h1 className="text-2xl font-bold">Welcome Home</h1>;
const Dashboard = () => <h1 className="text-2xl font-bold">User Dashboard</h1>;
const Settings = () => <h1 className="text-2xl font-bold">App Settings</h1>;
const NotFound = () => <h1 className="text-2xl font-bold text-red-500">404 - Page Not Found</h1>;

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* MainLayout wraps all these routes */}
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} /> {/* "index" means path="/" */}
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="settings" element={<Settings />} />
          
          {/* Catch-all for undefined routes */}
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
