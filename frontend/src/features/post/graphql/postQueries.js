import { gql } from '@apollo/client';

export const GET_ALL_POSTS = gql`
query MyQuery {
  UsersPostConnection {
    edges {
      node {
        title
        id
        createdBy {
          username
          name
          id
        }
        visibility
      }
    }
  }
}
`;

export const GET_USER_POSTS = gql`
query GetUserPosts($first: Int, $after: String) {
  UsersPostConnection(first: $first, after: $after) {
    edges {
      node {
        id
        title
        description
        visibility
        createdBy {
          id
          username
          name
        }
      }
    }
  }
}
`;
