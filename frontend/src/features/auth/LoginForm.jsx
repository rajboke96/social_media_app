import { useState } from 'react';
import { LOGIN_MUTATION } from './graphql/authQueries';
import { authClient } from '../../lib/authApolloClient';
import { useNavigate, Link } from 'react-router-dom';
import style from './auth.module.css';

function LoginForm() {
  const [form, setForm] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await authClient.mutate({
        mutation: LOGIN_MUTATION,
        variables: { data: { username: form.username, password: form.password } },
      });
      navigate('/');
    } catch (e) {
      setError(e.message || 'Login failed');
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={style.authPage}>
      <div className={style.authCard}>
        <h2>Sign in</h2>
        <form onSubmit={handleSubmit} className={style.authForm}>
          <label>
            Username or email
            <input name="username" value={form.username} onChange={handleChange} required />
          </label>
          <label>
            Password
            <input type="password" name="password" value={form.password} onChange={handleChange} required />
          </label>
          <button type="submit" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
          {error && <p className={style.error}>{error}</p>}
        </form>
        <div className={style.oauthRow}>
          <a href="http://localhost:8000/auth/login/google" className={style.googleButton}>Continue with Google</a>
        </div>
        <p>
          Don&apos;t have an account? <Link to="/signup">Create one</Link>
        </p>
      </div>
    </div>
  );
}

export default LoginForm;
