import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@apollo/client/react';
import { GET_USER_BY_USERNAME, GET_USER_POSTS, GET_USER_FRIENDS } from '../../features/user/graphql/userQueries';
import { FeedList } from '../../features/post';
import { useState } from 'react';
import style from './style.module.css';

function UserProfileDetails() {
  const { user_name } = useParams();
  const [activeTab, setActiveTab] = useState('posts');

  const { data: userData, loading: userLoading } = useQuery(GET_USER_BY_USERNAME, {
    variables: { username: user_name },
  });
  const { data: postsData, loading: postsLoading } = useQuery(GET_USER_POSTS, {
    variables: { username: user_name, first: 20 },
    skip: activeTab !== 'posts',
  });

  const { data: friendsData, loading: friendsLoading } = useQuery(GET_USER_FRIENDS, {
    variables: { username: user_name, first: 50 },
    skip: activeTab !== 'friends',
  });
  console.log('userData:', userData);
  if (userLoading) return <div className={style.container}>Loading user...</div>;
  if (!userData?.getUserByUsername) {
    return <div className={style.container}>User not found</div>;
  }

  const user = userData.getUserByUsername.username;

  const posts = postsData?.UsersPostConnection?.edges || [];
  const friends = friendsData?.UserFriendsConnection?.edges || [];

  return (
    <div className={style.container}>
      <div className={style.tabs}>
        <button 
          className={`${style.tab} ${activeTab === 'posts' ? style.activeTab : ''}`}
          onClick={() => setActiveTab('posts')}
        >
          Posts ({user?.postsCount ?? 0})
        </button>
        <button 
          className={`${style.tab} ${activeTab === 'friends' ? style.activeTab : ''}`}
          onClick={() => setActiveTab('friends')}
        >
          Friends ({friends.length})
        </button>
      </div>

      {activeTab === 'posts' && (
        <div className={style.section}>
          {postsLoading ? (
            <p>Loading posts...</p>
          ) : posts.length === 0 ? (
            <p className={style.empty}>No posts yet</p>
          ) : (
            <div className={style.postsGrid}>
              {posts.map(({ node }) => (
                <div key={node.id} className={style.postCard}>
                  <h3>{node.title}</h3>
                  <p>{node.description || 'No description'}</p>
                  {node.media?.length > 0 && (
                    <div className={style.postMedia}>
                      {node.media.map((m) => (
                        <img key={m.id} src={m.feedUrl || m.url} alt={m.name} />
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'friends' && (
        <div className={style.section}>
          {friendsLoading ? (
            <p>Loading friends...</p>
          ) : friends.length === 0 ? (
            <p className={style.empty}>No friends yet</p>
          ) : (
            <div className={style.friendsGrid}>
              {friends.map(({ node }) => (
                <div key={node.friend.id} className={style.friendCard}>
                  <div className={style.friendAvatar}>
                    {node.friend.name?.[0] || node.friend.username?.[0] || '?'}
                  </div>
                  <div className={style.friendName}>
                    <Link to={`/${node.friend.username}`}>{node.friend.name || node.friend.username}</Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default UserProfileDetails;
