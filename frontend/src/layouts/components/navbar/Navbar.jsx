import { NavLink } from "react-router-dom"
import style from "./style.module.css"

function Navbar(){
    return (
        <>
            <div className={style.navbarcontainer}>
                <nav className={style.navbar}>
                    <div className={style.homecontainer}>
                        <div className={style.applogo}>
                            
                        </div>
                    </div>
                    <ul className={style.nav}>
                        <li className={style.navitem}><NavLink to="/">Home</NavLink></li>
                        <li className={style.navitem}><NavLink to="#">Profile</NavLink></li>
                        <li className={style.navitem}><NavLink to="/friends">Friends</NavLink></li>
                        <li className={style.navitem}><NavLink to="#">My Posts</NavLink></li>
                        <li className={style.navitem}><NavLink to="#">Notifications</NavLink></li>
                    </ul>
                    <div className={style.searchbox}>
                        <input type="text" placeholder="search"/>
                        {/* <input type="button" value="Search"/> */}
                    </div>
                </nav>
            </div>
        </>
    )
}

export default Navbar