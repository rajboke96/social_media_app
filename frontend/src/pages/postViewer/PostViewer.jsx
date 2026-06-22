import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@apollo/client/react';
import { useState } from 'react';
import { GET_USER_POST } from '../../features/post/graphql/feedQueries';
import style from './style.module.css';

function PostViewer() {
  const { postId } = useParams();
  console.log("Post ID from URL:", postId);
  const navigate = useNavigate();
  const { data, loading, error } = useQuery(GET_USER_POST, {
    variables: { postId: postId },
  });
  const [currentIndex, setCurrentIndex] = useState(0);
  if (loading) return <div className={style.container}>Loading...</div>;
  if (error) return <div className={style.container}>Error: {error.message}</div>;

  const post = data?.getUserPost;
  if (!post) return <div className={style.container}>Post not found</div>;

  const images = post.media?.length > 0 ? post.media : [];

  const goNext = () => {
    setCurrentIndex((prev) => (prev + 1) % images.length);
  };

  const goPrev = () => {
    setCurrentIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  const authorName = post.createdBy?.name || post.createdBy?.username || 'Unknown';

  return (
    <div className={style.container}>
      <button className={style.backBtn} onClick={() => navigate(-1)}>
        ← Back
      </button>

      <div className={style.viewerLayout}>
        <div className={style.imageSection}>
          {images.length > 0 ? (
            <div className={style.imageSlider}>
              <button className={style.navBtn} onClick={goPrev}>‹</button>
              <img
                src={images[currentIndex]?.feedUrl || images[currentIndex]?.url}
                alt={post.title}
                className={style.mainImage}
              />
              <button className={style.navBtn} onClick={goNext}>›</button>
            </div>
          ) : (
            <div className={style.noImage}>No images</div>
          )}

          {images.length > 1 && (
            <div className={style.thumbnails}>
              {images.map((img, idx) => (
                <img
                  key={img.id || idx}
                  src={img.thumbnailUrl || img.feedUrl || img.url}
                  alt=""
                  className={`${style.thumb} ${idx === currentIndex ? style.activeThumb : ''}`}
                  onClick={() => setCurrentIndex(idx)}
                />
              ))}
            </div>
          )}
        </div>

        <div className={style.infoSection}>
          <div className={style.header}>
            <div className={style.author}>
              <span className={style.authorName}>{authorName}</span>
              <span className={style.time}>{new Date(post.createdAt).toLocaleDateString()}</span>
            </div>
          </div>

          <h2 className={style.title}>{post.title}</h2>
          {post.description && <p className={style.description}>{post.description}</p>}

          <div className={style.stats}>
            <span>{post.likeCount} Likes</span>
            <span>{post.commentCount} Comments</span>
          </div>

          <div className={style.comments}>
            <h3>Comments</h3>
            {post.comments?.length > 0 ? (
              post.comments.map((comment) => (
                <div key={comment.id} className={style.comment}>
                  <span className={style.commentUser}>{comment.user?.name || comment.user?.username}</span>
                  <p className={style.commentText}>{comment.text}</p>
                  <span className={style.commentTime}>
                    {new Date(comment.createdAt).toLocaleDateString()}
                  </span>
                </div>
              ))
            ) : (
              <p className={style.noComments}>No comments yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PostViewer;
