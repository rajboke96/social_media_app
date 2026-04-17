import { gql } from '@apollo/client';

// Keep queries close to the hook that uses them
export const GET_ALL_POSTS = gql`
query MyQuery {
  allUserPosts {
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