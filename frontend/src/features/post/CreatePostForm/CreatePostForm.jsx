import { useState, useRef } from 'react';
import { useMutation } from '@apollo/client/react';
import { CREATE_POST_MUTATION } from '../graphql/postMutations';
import style from './style.module.css';

function CreatePostForm({ onCreated }) {
  const [form, setForm] = useState({ title: '', description: '', visibility: 'PUBLIC', alt: '' });
  const [images, setImages] = useState([]);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const [createPost, { loading }] = useMutation(CREATE_POST_MUTATION);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleFiles = (event) => {
    const newFiles = Array.from(event.target.files);
    setImages((prev) => [...prev, ...newFiles]);
    event.target.value = '';
  };

  const removeImage = (index) => {
    setImages((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    if (!form.title.trim()) {
      setError('Please provide a title.');
      return;
    }

    try {
      const variables = {
        data: {
          title: form.title,
          description: form.description,
          visibility: form.visibility,
          alt: form.alt,
          image: images.length ? images : undefined,
        },
      };

      await createPost({ variables });
      setForm({ title: '', description: '', visibility: 'PUBLIC', alt: '' });
      setImages([]);
      if (onCreated) onCreated();
    } catch (err) {
      setError(err.message || 'Could not create post.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className={style.createPostForm}>
      <h3>Create post</h3>
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
      <label>
        Image alt text
        <input name="alt" value={form.alt} onChange={handleChange} />
      </label>

      <div className={style.imageSection}>
        <label className={style.imageLabel}>Images</label>
        <div className={style.imageGrid}>
          {images.map((file, index) => (
            <div key={index} className={style.imageCard}>
              <img
                src={URL.createObjectURL(file)}
                alt={file.name}
                className={style.preview}
              />
              <button
                type="button"
                className={style.removeBtn}
                onClick={() => removeImage(index)}
              >
                -
              </button>
            </div>
          ))}
          <button
            type="button"
            className={style.addImageBtn}
            onClick={() => fileInputRef.current?.click()}
          >
            +
          </button>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          onChange={handleFiles}
          className={style.hiddenInput}
        />
      </div>

      <button type="submit" disabled={loading}>{loading ? 'Posting...' : 'Create post'}</button>
      {error && <div className={style.error}>{error}</div>}
    </form>
  );
}

export default CreatePostForm;
