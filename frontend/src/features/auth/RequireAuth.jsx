import { useQuery } from '@apollo/client/react';
import { Navigate, useLocation } from 'react-router-dom';
import { ME_QUERY } from './graphql/authQueries';

function RequireAuth({ children }) {
  const location = useLocation();
  const { data, loading, error } = useQuery(ME_QUERY, {
    fetchPolicy: 'network-only',
  });

  if (loading) {
    return <div>Checking authentication...</div>;
  }

  if (error || !data?.me) {
    console.error('Authentication check failed:', error);
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
}

export default RequireAuth;
