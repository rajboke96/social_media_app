import {Outlet} from "react-router-dom"
import Sidebar from "../../../components/sidebar/Sidebar"
import style from "./style.module.css"

function MainContainer(){
    return (
        <div className={style.maincontainer}>
            <Sidebar />
            <div className={style.maincontent}>
                {/* This is where your individual pages (Dashboard, Settings, etc.) will render */}
                <Outlet />
            </div>
        </div>
    )
}

export default MainContainer