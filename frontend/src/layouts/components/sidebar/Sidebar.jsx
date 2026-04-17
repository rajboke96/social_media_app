import MainMenu from "../menus/MainMenu/MainMenu"
import FriendsMenu from "../menus/FriendsMenu/FriendsMenu";
import AllFriendsMenu from "../menus/AllFriendsMenu/AllFriendsMenu";
import style from "./style.module.css"
import { useLocation } from "react-router-dom"

function Sidebar(){
    const { pathname } = useLocation();

    if (pathname.startsWith('/friends/list')) {
        var menu=<AllFriendsMenu />; // Only shows when in /friends section
    } else if(pathname.startsWith('/friends')){
        var menu=<FriendsMenu />; // Only shows when in /friends section
    }
    else var menu=<MainMenu />; // Default menu for other pages
    return (
        <div className={style.sidebar}>
            {menu}
        </div>
    )
}

export default Sidebar