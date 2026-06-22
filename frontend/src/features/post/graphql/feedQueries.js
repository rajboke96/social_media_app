import { gql } from '@apollo/client';

export const GET_USER_FEED = gql`
query GetUserFeed($first: Int, $after: String) {
  getFeedsForUser(first: $first, after: $after) {
    edges {
      node {
        id
        title
        description
        createdBy {
          id
          username
          name
        }
        visibility
        createdAt
        media {
          id
          name
          type
          feedUrl
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
`;

export const GET_USER_POST = gql`
query GetUserPost($postId: ID!) {
  getUserPost(postId: $postId) {
    id
    title
    description
    visibility
    createdAt
    likeCount
    commentCount
    comments {
      id
      text
      createdAt
      user {
        id
        username
        name
      }
    }
    createdBy {
      id
      username
      name
    }
    media {
      id
      name
      type
      url
      feedUrl
      thumbnailUrl
      blurUrl
    }
  }
}
`;
