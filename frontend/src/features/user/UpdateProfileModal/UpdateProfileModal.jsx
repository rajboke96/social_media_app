import { useState, useRef } from 'react';
import { useMutation } from '@apollo/client/react';
import { UPDATE_PROFILE, GET_USER_PROFILE } from '../graphql/userQueries';
import { useQuery, useApolloClient } from '@apollo/client/react';
import Modal from '../../../components/Modal/Modal';
import style from './UpdateProfileModal.module.css';

function UpdateProfileModal({ open, onClose, onUpdated }) {
  const [bio, setBio] = useState('');
  const [cityId, setCityId] = useState('');
  const [profilePic, setProfilePic] = useState(null);
  const [coverPic, setCoverPic] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const client = useApolloClient();

  const profileInputRef = useRef(null);
  const coverInputRef = useRef(null);

  const [updateProfile] = useMutation(UPDATE_PROFILE);

  const handleFileChange = (setter) => (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setter(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const variables = {
        data: {
          profileBio: bio || undefined,
          cityId: cityId ? Number(cityId) : undefined,
          profilePicImg: profilePic || undefined,
          coverPicImg: coverPic || undefined,
        },
      };

      await updateProfile({ variables });
      if (onUpdated) onUpdated();
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to update profile.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <form onSubmit={handleSubmit} className={style.form}>
        <h3 className={style.title}>Edit Profile</h3>

        <label className={style.label}>
          <span>Bio</span>
          <textarea
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            placeholder="Write something about yourself"
            maxLength={300}
          />
        </label>

        <label className={style.label}>
          <span>Profile Photo</span>
          <input
            ref={profileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileChange(setProfilePic)}
            className={style.fileInput}
          />
          {profilePic && (
            <div className={style.previewRow}>
              <img src={URL.createObjectURL(profilePic)} alt="Profile preview" className={style.preview} />
              <button type="button" onClick={() => { setProfilePic(null); profileInputRef.current.value = ''; }} className={style.removeBtn}>×</button>
            </div>
          )}
        </label>

        <label className={style.label}>
          <span>Cover Photo</span>
          <input
            ref={coverInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileChange(setCoverPic)}
            className={style.fileInput}
          />
          {coverPic && (
            <div className={style.previewRow}>
              <img src={URL.createObjectURL(coverPic)} alt="Cover preview" className={style.coverPreview} />
              <button type="button" onClick={() => { setCoverPic(null); coverInputRef.current.value = ''; }} className={style.removeBtn}>×</button>
            </div>
          )}
        </label>

        <label className={style.label}>
          <span>City ID</span>
          <input
            type="number"
            value={cityId}
            onChange={(e) => setCityId(e.target.value)}
            placeholder="Enter city ID"
          />
        </label>

        {error && <div className={style.error}>{error}</div>}

        <div className={style.actions}>
          <button type="button" onClick={onClose} className={style.cancelBtn}>Cancel</button>
          <button type="submit" disabled={loading} className={style.submitBtn}>
            {loading ? 'Saving...' : 'Save Profile'}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default UpdateProfileModal;
