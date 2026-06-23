import style from "./style.module.css"
import { NavLink } from "react-router-dom"
import { useQuery } from "@apollo/client/react"
import { GET_MY_PROFILE, GET_CURRENT_USER } from "../../../../features/user/graphql/userQueries"


function MainMenu(){
    const { data: currentUserData } = useQuery(GET_CURRENT_USER);
    const currentUsername = currentUserData?.me?.username;
    const { data, loading } = useQuery(GET_MY_PROFILE, {
    variables: { userName: currentUsername },
});
    const profile = data?.getUserProfile;
    const user = profile?.user;
    const profilePic = profile?.profilePic;
    const displayName = user?.name || user?.username || currentUsername;
    const avatarSrc = profilePic?.thumbnailUrl || profilePic?.feedUrl || profilePic?.url;

    if (loading) return <ul className={style.mainMenu}><li className={style.menuitem}>Loading...</li></ul>;

    return (
        <ul className={style.mainMenu}>
            <li className={style.menuitem}>
                <div className={style.user}>
                    <NavLink to={`/profile`}>
                        <img width="100" height="100" src={avatarSrc} alt="" />
                    </NavLink>
                    <NavLink to={`/profile`}>{displayName}</NavLink>
                </div>
            </li>
            {/* <li className={style.menuitem}><NavLink to="/friends">Friends</NavLink></li> */}
        </ul>
    )
}

export default MainMenu