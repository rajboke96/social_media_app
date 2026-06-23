import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation } from '@apollo/client/react';
import { useState } from 'react';
import { GET_USER_PROFILE, GET_CURRENT_USER } from '../../../../../../features/user/graphql/userQueries';
import UpdateProfileModal from '../../../../../../features/user/UpdateProfileModal/UpdateProfileModal';
import style from './style.module.css';

function ProfileHeader() {
    const { user_name } = useParams();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const { data, loading, error, refetch } = useQuery(GET_USER_PROFILE, {
        variables: { userName: user_name },
    });
    
    const { data: currentUserData } = useQuery(GET_CURRENT_USER);
    const currentUsername = currentUserData?.me?.username;
    const isOwnProfile = currentUsername && user_name && currentUsername.toLowerCase() === user_name.toLowerCase();

    const profile = data?.getUserProfile;
    const user = profile?.user;

    if (loading) return <div className={style.profileHeader}>Loading...</div>;
    if (error) return <div className={style.profileHeader}>Error: {error.message}</div>;
    if (!profile || !user) {
        return (
            <div className={style.profileHeader}>
                <div className={style.emptyProfile}>
                    <div className={style.emptyCover}>
                        <div className={style.emptyCoverText}>No Cover Photo</div>
                        <button className={style.addBtn} onClick={() => setIsModalOpen(true)}>+ Add Cover Photo</button>
                    </div>
                    <div className={style.emptySummary}>
                        <div className={style.emptyAvatar}>
                            <span className={style.emptyAvatarText}>?</span>
                        </div>
                        <div className={style.emptyInfo}>
                            <h2 className={style.emptyName}>{user_name}</h2>
                            <p className={style.emptyHint}>Complete your profile by adding photos and information</p>
                            {isOwnProfile && (
                                <div className={style.emptyActions}>
                                    <button className={style.primaryBtn} onClick={() => setIsModalOpen(true)}>Add Profile Photo</button>
                                    <button className={style.secondaryBtn} onClick={() => setIsModalOpen(true)}>Edit Profile</button>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
                {isOwnProfile && (
                    <UpdateProfileModal open={isModalOpen} onClose={() => setIsModalOpen(false)} onUpdated={() => { refetch(); setIsModalOpen(false); }} />
                )}
            </div>
        );
    }

    const coverSrc = profile.coverPic?.feedUrl || profile.coverPic?.url || '/static/images/cover_pic.jpg';
    const avatarSrc = profile.profilePic?.thumbnailUrl || profile.profilePic?.feedUrl || profile.profilePic?.url || '/static/images/profile_img.jpg';
    const displayName = user.name || user.username || user_name;

    return (
        <div className={style.profileHeader}>
            <div className={style.coverpicContainer}>
                <div className={style.coverpic}>
                    <img src={coverSrc} alt="Cover" />
                    {isOwnProfile && <button onClick={() => setIsModalOpen(true)}>Add Cover Photo</button>}
                </div>
            </div>
            <div className={style.centerContainer}>
                <div className={style.summaryContainer}>
                    <div className={style.summary}>
                        <div className={style.profileImage}>
                            <img src={avatarSrc} alt={displayName} />
                        </div>
                        <div className={style.summaryContentContainer}>
                            <div className={style.summaryContent}>
                                <div className={style.header}>
                                    <div className={style.userDetail}>
                                        <div className={style.userFullName}>
                                            {displayName}
                                        </div>
                                        <div className={style.userMeta}>
                                            <span className={style.friendsCount}>
                                                View friends
                                            </span>
                                        </div>
                                    </div>
                                    <div className={style.userOptions}>
                                        <button onClick={() => setIsModalOpen(true)}>+ Add to story</button>
                                        {isOwnProfile && <button onClick={() => setIsModalOpen(true)}>Edit profile</button>}
                                        <button>Friends suggestions</button>
                                    </div>
                                </div>
                                <div className={style.footer}>
                                    {profile.profileBio && <p className={style.bio}>{profile.profileBio}</p>}
                                    {profile.city && <ul>
                                        <li>{profile.city.name}</li>
                                    </ul>}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className={style.centerContainer}>
                <div className={style.menuContainer}>
                    <div className={style.menu}>
                        <ul>
                            <li><Link to="." state={{ tab: 'posts' }}>Posts</Link></li>
                            <li><Link to="friends">Friends</Link></li>
                            <li><Link to="about">About</Link></li>
                            <li><Link to="photos">Photos</Link></li>
                        </ul>
                    </div>
                </div>
            </div>
            {isOwnProfile && (
                <UpdateProfileModal open={isModalOpen} onClose={() => setIsModalOpen(false)} onUpdated={() => { refetch(); setIsModalOpen(false); }} />
            )}
            {!isOwnProfile && (
                <UpdateProfileModal open={isModalOpen} onClose={() => setIsModalOpen(false)} />
            )}
        </div>
    )
}
export default ProfileHeader
