import { useState, useRef, useEffect } from 'react';
import { useLazyQuery } from '@apollo/client/react';
import { SEARCH_USERS } from '../../../features/user/graphql/userQueries';
import style from './style.module.css';

function SearchBar() {
  const [searchText, setSearchText] = useState('');
  const [showResults, setShowResults] = useState(false);
  const [searchUsers, { loading, error, data }] = useLazyQuery(SEARCH_USERS, {
    fetchPolicy: 'network-only',
  });
  const searchRef = useRef(null);

  const handleSearch = (value) => {
    setSearchText(value);
    if (value.trim().length > 0) {
      setShowResults(true);
      searchUsers({
        variables: { search: value.trim(), first: 8 },
      });
    } else {
      setShowResults(false);
    }
  };

  const handleResultClick = (user) => {
    console.log('Selected user', user);
    setSearchText('');
    setShowResults(false);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowResults(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={style.searchWrapper} ref={searchRef}>
      <input
        type="text"
        placeholder="Search users..."
        value={searchText}
        onChange={(e) => handleSearch(e.target.value)}
        className={style.searchInputField}
      />

      {showResults && (
        <div className={style.resultsDropdown}>
          {loading && (
            <div className={style.loadingMessage}>
              <span>Searching...</span>
            </div>
          )}

          {error && (
            <div className={style.errorMessage}>
              Error: {error.message}
            </div>
          )}

          {!loading && !error && data?.searchUser?.edges?.length === 0 && (
            <div className={style.noResults}>
              No users found
            </div>
          )}

          {data?.searchUser?.edges && data.searchUser.edges.length > 0 && (
            <div className={style.resultsList}>
              {data.searchUser.edges.map(({ node }) => (
                <button
                  key={node.id}
                  className={style.resultCard}
                  onClick={() => handleResultClick(node)}
                >
                  <div className={style.resultHeader}>
                    <span className={style.resultName}>{node.name || node.username}</span>
                    <span className={style.resultStatus}>{node.accountStatus}</span>
                  </div>
                  <div className={style.resultUsername}>@{node.username}</div>
                  {node.email && <div className={style.resultEmail}>{node.email}</div>}
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default SearchBar;
