import { useState } from 'react';
import { SIGNUP_MUTATION } from './graphql/authQueries';
import { authClient } from '../../lib/authApolloClient';
import { useNavigate, Link } from 'react-router-dom';
import style from './auth.module.css';

function SignupForm() {
  const [form, setForm] = useState({ firstname: '', username: '', password: '', confirmPassword: '' });
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

    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await authClient.mutate({
        mutation: SIGNUP_MUTATION,
        variables: { data: { firstname: form.firstname, username: form.username, password: form.password } },
      });
      navigate('/login');
    } catch (e) {
      setError(e.message || 'Signup failed');
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={style.authPage}>
      <div className={style.authCard}>
        <h2>Create account</h2>
        <form onSubmit={handleSubmit} className={style.authForm}>
          <label>
            First name
            <input name="firstname" value={form.firstname} onChange={handleChange} required />
          </label>
          <label>
            Username or email
            <input name="username" value={form.username} onChange={handleChange} required />
          </label>
          <label>
            Password
            <input type="password" name="password" value={form.password} onChange={handleChange} required />
          </label>
          <label>
            Confirm password
            <input type="password" name="confirmPassword" value={form.confirmPassword} onChange={handleChange} required />
          </label>
          <button type="submit" disabled={loading}>{loading ? 'Creating account...' : 'Create account'}</button>
          {error && <p className={style.error}>{error}</p>}
        </form>
        <p>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}

export default SignupForm;
