import style from './style.module.css'

function ProfileHeader(){
    return (
        <div className={style.profileHeader}>
            <div className={style.coverpicContainer}>
                <div className={style.coverpic}>
                    <img src="../../static/images/cover_pic.jpg" alt="" />
                    <button>Add Cover Photo</button>
                </div>
            </div>
            <div className={style.centerContainer}>
                <div className={style.summaryContainer}>
                    <div className={style.summary}>
                        <div className={style.profileImage}>
                            <img src="../../static/images/profile_img.jpg" alt="" />
                        </div>
                        <div className={style.summaryContentContainer}>
                            <div className={style.summaryContent}>
                                <div className={style.header}>
                                    <div className={style.userDetail}>
                                        <div className={style.userFullName}>
                                            Rajendra Boke
                                        </div>
                                        <div className={style.totalFriends}>
                                            1.5k friends
                                        </div>
                                    </div>
                                    <div className={style.userOptions}>
                                        <button>+ Add to story</button>
                                        <button>Edit profile</button>
                                        <button>Friends suggestions</button>
                                    </div>
                                </div>
                                <div className={style.footer}>
                                    <ul>
                                        <li>Mumbai</li>
                                        <li>
                                            SM Shetty College of Science,Commerce & Management Studies, Mumbai
                                        </li>
                                        </ul>
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
                            <li>All</li>
                            <li>About</li>
                            <li>Friends</li>
                            <li>Photos</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default ProfileHeader