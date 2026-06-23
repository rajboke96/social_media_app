import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout/MainLayout';
import ProfileLayout from './layouts/ProfileLayout/ProfileLayout';
import { Feeds } from './pages/feeds';
import LoginPage from './pages/auth/LoginPage';
import SignupPage from './pages/auth/SignupPage';
import PostViewer from './pages/postViewer/PostViewer';
import UserProfileDetails from './pages/userProfile/UserProfileDetails';
import UserAbout from './pages/userProfile/UserAbout';
import UserFriends from './pages/userProfile/UserFriends';
import UserPhotos from './pages/userProfile/UserPhotos';
import ProfileRedirect from './pages/profileRedirect/ProfileRedirect';
import RequireAuth from './features/auth/RequireAuth';
import { ApolloProvider } from '@apollo/client/react';
import { authClient, appClient } from './lib/authApolloClient';
import { Outlet } from 'react-router-dom';

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
        
        {/* 🔐 AUTH CLIENT ROUTES */}
        {/* We use an empty layout route element to safely inject the provider inside <Routes> */}
        <Route element={<ApolloProvider client={authClient}><Outlet /></ApolloProvider>}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
        </Route>

        {/* 📦 APP CLIENT ROUTES */}
        {/* This injects the appClient context to all underlying protected application routes */}
        <Route element={<ApolloProvider client={appClient}><Outlet /></ApolloProvider>}>
          
          {/* Main Application Layout Routes */}
          <Route path="/" element={<RequireAuth><MainLayout /></RequireAuth>}>
            <Route index element={<Home />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="settings" element={<Settings />} />
            <Route path="feeds" element={<Feeds />} />
            <Route path="post/:postId" element={<PostViewer />} />
            <Route path="profile" element={<ProfileRedirect />} />
            
            {/* Catch-all for undefined routes inside MainLayout context */}
            <Route path="*" element={<NotFound />} />
          </Route>

          {/* Friends Layout Routes */}
          <Route path="/friends" element={<RequireAuth><MainLayout /></RequireAuth>}>
            <Route index element={<Friends />} />
            <Route path="list" element={<AllFriends />} />
            <Route path="requests" element={<FriendRequests />} />
          </Route>

          {/* User Profile Layout Routes */}
          <Route path="/:user_name" element={<RequireAuth><ProfileLayout /></RequireAuth>}>
            <Route index element={<UserProfileDetails />} />
            <Route path="about" element={<UserAbout />} />
            <Route path="friends" element={<UserFriends />} />
            <Route path="photos" element={<UserPhotos />} />
          </Route>

        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;
