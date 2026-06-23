import { useParams } from 'react-router-dom';
import { useQuery } from '@apollo/client/react';
import { GET_USER_FRIENDS } from '../../features/user/graphql/userQueries';
import style from './style.module.css';

function UserFriends() {
  const { user_name } = useParams();
  const { data, loading, error } = useQuery(GET_USER_FRIENDS, {
    variables: { username: user_name, first: 50 },
  });

  if (loading) return <div className={style.container}>Loading friends...</div>;
  if (error) return <div className={style.container}>Error: {error.message}</div>;

  const friends = data?.UserFriendsConnection?.edges || [];

  return (
    <div className={style.container}>
      <h2>Friends</h2>
      {friends.length === 0 ? (
        <p className={style.empty}>No friends yet</p>
      ) : (
        <div className={style.friendsGrid}>
          {friends.map(({ node }) => (
            <div key={node.friend.id} className={style.friendCard}>
              <div className={style.friendAvatar}>
                {node.friend.name?.[0] || node.friend.username?.[0] || '?'}
              </div>
              <div className={style.friendName}>
                {node.friend.name || node.friend.username}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default UserFriends;
