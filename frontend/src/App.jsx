import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import {Feeds} from './pages/feeds';

// Simple Page Components
const Home = () => (
  <>
    <Feeds />
  </>
);
const Dashboard = () => <h1 className="text-2xl font-bold">User Dashboard</h1>;
const Settings = () => <h1 className="text-2xl font-bold">App Settings</h1>;
const NotFound = () => <h1 className="text-2xl font-bold text-red-500">404 - Page Not Found</h1>;

const Friends = () => <h1 className="text-2xl font-bold">Friends Page</h1>;
const AllFriends = () => <h3>Select people's names to preview their profile.</h3>;
const FriendRequests = () => <h1 className="text-2xl font-bold">Friend requests</h1>;

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* MainLayout wraps all these routes */}
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} /> {/* "index" means path="/" */}
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="settings" element={<Settings />} />
          <Route path="feeds" element={<Feeds />} />
          
          {/* Catch-all for undefined routes */}
          <Route path="*" element={<NotFound />} />
        </Route>
        {/* The FriendsLayout will always show when the URL starts with /friends */}
        <Route path="/friends" element={<MainLayout />}>
            <Route index element={<Friends />} /> {/* path="/friends" */}
            <Route path="list" element={<AllFriends />} /> {/* path="/friends/all" */}
            <Route path="requests" element={<FriendRequests />} /> {/* path="/friends/requests" */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
