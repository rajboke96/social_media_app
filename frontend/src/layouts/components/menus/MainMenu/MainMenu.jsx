import style from "./style.module.css"
import { NavLink } from "react-router-dom"

function MainMenu(){
    return (
        <ul className={style.mainMenu}>
            <li className={style.menuitem}>
                <div className={style.user}>
                    <img src="../static/images/617746637_25206255859071293_8894525724258327052_n (1).jpg" alt="" />
                    <NavLink to="#">Rajendra Boke</NavLink>
                </div>
            </li>
            <li className={style.menuitem}><NavLink to="/friends">Friends</NavLink></li>
            <li className={style.menuitem}><NavLink to="/groups">Groups</NavLink></li>
            <li className={style.menuitem}><NavLink to="/saved">Saved</NavLink></li>
            <li className={style.menuitem}><NavLink to="/feeds">Feeds</NavLink></li>
        </ul>
    )
}

export default MainMenu