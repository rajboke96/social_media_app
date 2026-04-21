import {Outlet} from "react-router-dom"
import style from "./style.module.css"

function ProfileContent(){
    return (
        <div className={style.centerContainer}>
            <div className={style.profileContent}>
                <div className={style.menuContent}>
                    <Outlet />
                </div>
            </div>
        </div>
    )
}

export default ProfileContent
