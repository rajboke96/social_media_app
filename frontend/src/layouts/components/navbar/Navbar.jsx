import { NavLink, useNavigate } from "react-router-dom"
import { useMutation } from '@apollo/client/react';
import { LOGOUT_MUTATION } from '../../../features/auth/graphql/authQueries';
import style from "./style.module.css"
import SearchBar from "./SearchBar"

function Navbar(){
    const navigate = useNavigate();
    const [logout] = useMutation(LOGOUT_MUTATION, {
      onCompleted: () => navigate('/login'),
      onError: () => navigate('/login'),
    });

    const handleLogout = async () => {
      try {
        await logout();
      } catch (err) {
        console.error('Logout failed', err);
        navigate('/login');
      }
    };

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
                        <li className={style.navitem}><NavLink to="/profile">Profile</NavLink></li>
                        <li className={style.navitem}><button className={style.logoutButton} type="button" className={style.logoutButton} onClick={handleLogout}>
                            Logout
                          </button></li>
                    </ul>
                    <div className={style.searchbox}>
                        <SearchBar />
                    </div>
                </nav>
            </div>
        </>
    )
}

export default Navbar