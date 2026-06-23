import { useParams } from 'react-router-dom';
import { useQuery } from '@apollo/client/react';
import { GET_USER_PROFILE } from '../../features/user/graphql/userQueries';
import style from './style.module.css';

function UserAbout() {
  const { user_name } = useParams();
  const { data, loading, error } = useQuery(GET_USER_PROFILE, {
    variables: { userName: user_name },
  });

  if (loading) return <div className={style.container}>Loading...</div>;
  if (error) return <div className={style.container}>Error: {error.message}</div>;
  if (!data?.get_user_profile) return <div className={style.container}>User not found</div>;

  const profile = data.get_user_profile;
  const user = profile.user;

  return (
    <div className={style.container}>
      <h2>About</h2>
      <div className={style.aboutCard}>
        <div className={style.row}>
          <strong>Username:</strong> {user?.username}
        </div>
        <div className={style.row}>
          <strong>Name:</strong> {user?.name || 'Not set'}
        </div>
        <div className={style.row}>
          <strong>Email:</strong> {user?.email || 'Not set'}
        </div>
        <div className={style.row}>
          <strong>Bio:</strong> {profile.profileBio || 'Not set'}
        </div>
        <div className={style.row}>
          <strong>City:</strong> {profile.city?.name || 'Not set'}
        </div>
      </div>
    </div>
  );
}

export default UserAbout;
