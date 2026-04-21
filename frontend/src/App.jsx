import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout/MainLayout';
import ProfileLayout from './layouts/ProfileLayout/ProfileLayout';
import {Feeds} from './pages/feeds';

// Simple Page Components
const Home = () => (
  <>
    <Feeds />
  </>
);
const Dashboard = () => <h1 className="text-2xl font-bold">User Dashboard</h1>;
const Settings = () => <h1 className="text-2xl font-bold">App Settings</h1>;
const NotFound = () => <h1 className="text-2xl font-bold text-red-500">404 - Page Not Found</h1>;

const Friends = () => <h1 className="text-2xl font-bold">Friends Page</h1>;
const AllFriends = () => <h3>Select people's names to preview their profile.</h3>;
const FriendRequests = () => <h1 className="text-2xl font-bold">Friend requests</h1>;

const UserProfileDetails= () => <h1 className="text-2xl font-bold">UserProfileDetails Page</h1>;
const UserAbout= () => <><h1 className="text-2xl font-bold">UserAbout Page</h1><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima, maiores necessitatibus reiciendis aliquam facere quod a doloribus, itaque, labore harum perferendis veniam rem doloremque expedita eum accusantium illum obcaecati unde sequi. Aut, ut dolor? Odit, quis aliquam. Blanditiis facilis minus asperiores qui doloribus dolorem, aut debitis, necessitatibus repellat enim quas nesciunt dolorum dolore. Voluptates incidunt maxime facilis, qui culpa est molestiae asperiores veritatis ducimus earum eum eligendi doloribus delectus deserunt voluptatibus natus suscipit voluptate, nam officiis laborum illo? Ipsum rerum ipsam perferendis aspernatur similique delectus magni numquam dolorum labore non ullam nobis, vitae itaque rem et eaque earum ducimus quis! Tempore nobis ex asperiores amet itaque maiores corporis officiis vel, molestiae sapiente omnis fuga architecto, quaerat dolores accusantium dolorem ipsum cumque mollitia. Laborum, eaque sint! Exercitationem nemo dolorum a id! Eligendi, asperiores pariatur voluptas nisi perspiciatis porro perferendis facilis nam quaerat minus, inventore suscipit placeat! Rem, libero consectetur amet fugit modi saepe itaque corrupti vel, doloremque culpa quaerat voluptatibus maiores officiis sunt accusamus consequuntur perspiciatis voluptate maxime illum. Laudantium inventore optio harum vero fugit omnis quisquam ab placeat, similique in at. Cupiditate, animi cum inventore debitis magnam quibusdam sequi excepturi ipsam temporibus odio sapiente aperiam mollitia voluptatem officia, quo blanditiis qui eius expedita veniam, ut commodi laborum sit provident quis! Laboriosam ex incidunt amet alias voluptatem maiores dolor earum repellat sequi in nisi enim pariatur illum, quibusdam quo esse praesentium sed atque similique ut animi iusto nemo labore deserunt! Quasi quidem fuga odit maiores rerum quis, quod quas. Tempora eaque saepe nesciunt ea repellendus laboriosam alias eveniet. Itaque inventore, error nesciunt culpa ad eveniet qui. Explicabo quam, provident expedita quibusdam ex facilis, quo nam accusamus iusto itaque impedit rem nulla distinctio labore mollitia totam neque inventore illo quod rerum dolorum? Voluptatem amet ad nihil molestiae atque magnam, voluptate ipsum quam ducimus. Porro nihil odit neque facere. Vero ipsum, aut sapiente corporis dolor sunt quis inventore, odit sit provident non nam architecto illo saepe ab? Perspiciatis rerum at neque praesentium porro quas optio id corporis nisi culpa recusandae itaque aliquam, voluptatibus nam expedita, in architecto nulla! Enim vitae repellendus ratione a quia dolorem error doloremque praesentium ut aliquam, mollitia dolore natus id optio porro quidem earum dignissimos magnam officia fugiat. Reprehenderit enim eius neque maxime. Voluptatem, non. Tenetur repellat rerum omnis quasi temporibus tempora non optio unde corrupti tempore, ex libero, at praesentium maxime, nobis numquam in suscipit eligendi distinctio odit. Odio expedita natus assumenda explicabo? Quos aut ipsa et corporis voluptate ea quasi qui ratione nihil ex iste laborum, odit ipsam, tenetur placeat numquam blanditiis sint nostrum nesciunt. Tempore, odit mollitia. Accusamus, cum! Molestiae sed modi voluptas dignissimos fuga quos laudantium culpa voluptates atque. Perferendis doloribus qui sunt velit in distinctio eaque esse accusantium. Eius obcaecati aliquid ut asperiores ab debitis ipsam officia, dolor blanditiis, sapiente praesentium provident inventore. Ullam minima suscipit perspiciatis expedita ducimus, deleniti ipsum, eligendi praesentium adipisci explicabo porro ea, accusantium nobis aliquid excepturi voluptatum natus ab debitis repellendus sed nisi? Amet suscipit reiciendis sit aliquid ipsum!</p></>;
const UserFriends= () => <h1 className="text-2xl font-bold">UserFriends Page</h1>;
const UserPhotos= () => <h1 className="text-2xl font-bold">UserPhotos Page</h1>;

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* MainLayout wraps all these routes */}
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} /> {/* "index" means path="/" */}
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="settings" element={<Settings />} />
          <Route path="feeds" element={<Feeds />} />
          
          {/* Catch-all for undefined routes */}
          <Route path="*" element={<NotFound />} />
        </Route>
        {/* The FriendsLayout will always show when the URL starts with /friends */}
        <Route path="/friends" element={<MainLayout />}>
            <Route index element={<Friends />} /> {/* path="/friends" */}
            <Route path="list" element={<AllFriends />} /> {/* path="/friends/all" */}
            <Route path="requests" element={<FriendRequests />} /> {/* path="/friends/requests" */}
        </Route>
        <Route path="/:user_name" element={<ProfileLayout />}>
            <Route index element={<UserProfileDetails />} />
            <Route path='about' element={<UserAbout />} />
            <Route path="friends" element={<UserFriends />} />
            <Route path='photos' element={<UserPhotos />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
