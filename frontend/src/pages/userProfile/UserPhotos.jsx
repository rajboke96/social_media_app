import { useParams } from 'react-router-dom';
import { useQuery } from '@apollo/client/react';
import { GET_USER_POSTS } from '../../features/user/graphql/userQueries';
import style from './style.module.css';

function UserPhotos() {
  const { user_name } = useParams();
  const { data, loading, error } = useQuery(GET_USER_POSTS, {
    variables: { username: user_name, first: 50 },
  });

  if (loading) return <div className={style.container}>Loading photos...</div>;
  if (error) return <div className={style.container}>Error: {error.message}</div>;

  const posts = data?.UsersPostConnection?.edges || [];
  const allMedia = posts.flatMap(({ node }) => node.media || []);

  return (
    <div className={style.container}>
      <h2>Photos</h2>
      {allMedia.length === 0 ? (
        <p className={style.empty}>No photos yet</p>
      ) : (
        <div className={style.photosGrid}>
          {allMedia.map((m) => (
            <img key={m.id} src={m.feedUrl || m.url} alt={m.name} className={style.photo} />
          ))}
        </div>
      )}
    </div>
  );
}

export default UserPhotos;
