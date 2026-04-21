import {Outlet} from "react-router-dom"
import style from "./style.module.css"
import ProfileHeader from "./components/ProfileHeader/ProfileHeader"
import ProfileContent from "./components/ProfileContent/ProfileContent"

function ProfileContainer(){
    return (
        <div className={style.profileContainer}>
            <ProfileHeader />
            <ProfileContent />
        </div>
    )
}

export default ProfileContainer