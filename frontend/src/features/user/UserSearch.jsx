import { useState } from 'react';
import { useLazyQuery } from '@apollo/client/react';
import { SEARCH_USERS } from './graphql/userQueries';
import style from './style.module.css';

function UserSearch({ onSelectUser }) {
  const [searchText, setSearchText] = useState('');
  const [searchUsers, { loading, error, data }] = useLazyQuery(SEARCH_USERS, {
    fetchPolicy: 'network-only',
  });

  const onSearch = () => {
    if (!searchText.trim()) return;
    searchUsers({
      variables: { search: searchText.trim(), first: 20 },
    });
  };

  return (
    <div className={style.searchContainer}>
      <div className={style.searchInputGroup}>
        <input
          type="text"
          placeholder="Search users by name, username or email"
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          className={style.searchInput}
        />
        <button onClick={onSearch} className={style.searchButton}>
          Search
        </button>
      </div>

      {loading && <div className={style.status}>Loading users...</div>}
      {error && <div className={style.statusError}>Error: {error.message}</div>}

      {data?.searchUser?.edges?.length > 0 && (
        <div className={style.results}>
          {data.searchUser.edges.map(({ node }) => (
            <button
              key={node.id}
              className={style.resultItem}
              onClick={() => onSelectUser?.(node)}
            >
              <div className={style.resultName}>{node.name || node.username}</div>
              <div className={style.resultMeta}>{node.username}</div>
              <div className={style.resultMeta}>{node.email}</div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default UserSearch;
