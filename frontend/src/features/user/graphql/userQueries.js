import { gql } from '@apollo/client';

export const SEARCH_USERS = gql`
query SearchUsers($search: String!, $first: Int, $after: String) {
  searchUser(userSearchStr: $search, first: $first, after: $after) {
    edges {
      node {
        id
        username
        name
        email
        accountType
        accountStatus
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
`;
