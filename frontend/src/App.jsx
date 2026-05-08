import { Route, Routes } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import ProtectedRoute from './routes/ProtectedRoute';
import AdminUploadPanel from './pages/AdminUploadPanel';
import AnalyticsDashboard from './pages/AnalyticsDashboard';
import ChatDashboard from './pages/ChatDashboard';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<ChatDashboard />} />
        <Route path="/analytics" element={<AnalyticsDashboard />} />
        <Route
          path="/admin"
          element={
            <ProtectedRoute adminOnly>
              <AdminUploadPanel />
            </ProtectedRoute>
          }
        />
      </Route>
    </Routes>
  );
}
