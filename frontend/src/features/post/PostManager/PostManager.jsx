import { useState } from 'react';
import { useMutation, useQuery } from '@apollo/client/react';
import { GET_USER_POSTS } from '../graphql/postQueries';
import { CREATE_POST_MUTATION, UPDATE_POST_MUTATION, DELETE_POST_MUTATION } from '../graphql/postMutations';
import CreatePostForm from '../CreatePostForm/CreatePostForm';
import style from './style.module.css';

function PostManager() {
  const { data, loading, error, refetch } = useQuery(GET_USER_POSTS, { variables: { first: 20 } });
  const [activePost, setActivePost] = useState(null);
  const [updatePost] = useMutation(UPDATE_POST_MUTATION);
  const [deletePost] = useMutation(DELETE_POST_MUTATION);
  const [form, setForm] = useState({ title: '', description: '', visibility: 'PUBLIC' });
  const [message, setMessage] = useState(null);

  const handleEdit = (post) => {
    setActivePost(post);
    setForm({ title: post.title, description: post.description || '', visibility: post.visibility });
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleUpdate = async (event) => {
    event.preventDefault();
    setMessage(null);
    try {
      await updatePost({ variables: { data: { id: activePost.id, title: form.title, description: form.description, visibility: form.visibility } } });
      setMessage('Post updated successfully.');
      setActivePost(null);
      await refetch();
    } catch (err) {
      setMessage(err.message || 'Update failed.');
    }
  };

  const handleDelete = async (postId) => {
    setMessage(null);
    try {
      await deletePost({ variables: { postId } });
      setMessage('Post deleted successfully.');
      await refetch();
    } catch (err) {
      setMessage(err.message || 'Delete failed.');
    }
  };

  if (loading) return <div className={style.postManager}>Loading posts...</div>;
  if (error) return <div className={style.postManager}>Error loading your posts: {error.message}</div>;

  return (
    <div className={style.postManager}>
      <CreatePostForm onCreated={() => refetch()} />
      {message && <div className={style.message}>{message}</div>}
      {activePost && (
        <form onSubmit={handleUpdate} className={style.updateForm}>
          <h3>Edit post</h3>
          <label>
            Title
            <input name="title" value={form.title} onChange={handleChange} required />
          </label>
          <label>
            Description
            <textarea name="description" value={form.description} onChange={handleChange} />
          </label>
          <label>
            Visibility
            <select name="visibility" value={form.visibility} onChange={handleChange}>
              <option value="PUBLIC">Public</option>
              <option value="PRIVATE">Private</option>
            </select>
          </label>
          <div className={style.updateButtons}>
            <button type="submit">Save changes</button>
            <button type="button" onClick={() => setActivePost(null)}>Cancel</button>
          </div>
        </form>
      )}
      <div className={style.postList}>
        <h3>Your posts</h3>
        {data?.UsersPostConnection?.edges?.length ? (
          data.UsersPostConnection.edges.map(({ node }) => (
            <div key={node.id} className={style.postCard}>
              <div className={style.cardHeader}>
                <strong>{node.title}</strong>
                <div className={style.cardActions}>
                  <button onClick={() => handleEdit(node)}>Edit</button>
                  <button onClick={() => handleDelete(node.id)}>Delete</button>
                </div>
              </div>
              <p>{node.description || 'No description'}</p>
              <p className={style.visibility}>{node.visibility}</p>
            </div>
          ))
        ) : (
          <p>No posts yet. Create one above.</p>
        )}
      </div>
    </div>
  );
}

export default PostManager;
