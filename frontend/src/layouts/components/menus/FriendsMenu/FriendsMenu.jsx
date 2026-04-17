import { NavLink } from 'react-router-dom';
import style from './style.module.css'

const FriendsMenu = () => {
  return (
    <ul className={style.mainMenu}>
        <li className={style.menuitem}><NavLink to="/friends/requests">Friends Requests</NavLink></li>
        <li className={style.menuitem}><NavLink to="/friends/list">All Friends</NavLink></li>
        <li className={style.menuitem}><NavLink to="/friends/suggestions">Suggestions</NavLink></li>
    </ul>
  );
};

export default FriendsMenu;