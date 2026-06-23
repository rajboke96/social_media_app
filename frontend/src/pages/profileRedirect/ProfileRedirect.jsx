import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@apollo/client/react';
import { GET_CURRENT_USER } from '../../features/user/graphql/userQueries';

function ProfileRedirect() {
  const { data } = useQuery(GET_CURRENT_USER);
  const navigate = useNavigate();
  const username = data?.me?.username;

  useEffect(() => {
    if (username) {
      navigate(`/${username}`, { replace: true });
    }
  }, [username, navigate]);

  if (!username) return <div>Loading...</div>;
  return null;
}

export default ProfileRedirect;
