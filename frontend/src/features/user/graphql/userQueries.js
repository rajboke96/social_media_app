import { gql } from '@apollo/client';

export const GET_USER_PROFILE = gql`
query GetUserProfile($userName: String!) {
  getUserProfile(userName: $userName) {
    id
    profileBio
    profilePic {
      id
      url
      feedUrl
      thumbnailUrl
    }
    coverPic {
      id
      url
      feedUrl
    }
    user {
      id
      username
      name
      email
    }
    city {
      id
      name
    }
  }
}
`;

export const GET_USER_BY_USERNAME = gql`
query GetUserByUsername($username: String!) {
  getUserByUsername(username: $username) {
    id
    username
    name
    email
  }
}
`;

export const SEARCH_USERS = gql`
query SearchUsers($search: String!, $first: Int) {
  searchUser(userSearchStr: $search, first: $first) {
    edges {
      node {
        id
        username
        name
        email
        accountStatus
      }
    }
  }
}
`;

export const GET_USER_FRIENDS = gql`
query GetUserFriends($username: String!, $first: Int, $after: String) {
  UserFriendsConnection(first: $first, after: $after, username: $username) {
    edges {
      node {
        friend {
          id
          username
          name
          email
        }
        friendsAt
        status
      }
    }
  }
}
`;

export const GET_USER_POSTS = gql`
query GetUserPosts($username: String!, $first: Int, $after: String) {
  UsersPostConnection(first: $first, after: $after, username: $username) {
    edges {
      node {
        id
        title
        description
        visibility
        createdAt
        media {
          id
          name
          type
          feedUrl
          url
        }
      }
    }
  }
}
`;

export const UPDATE_PROFILE = gql`
mutation UpdateProfile($data: UpdateProfileInput!) {
  updateUserProfile(data: $data) {
    id
    profileBio
    profilePic {
      id
      url
      feedUrl
      thumbnailUrl
    }
    coverPic {
      id
      url
      feedUrl
    }
    user {
      id
      username
      name
    }
  }
}
`;

export const GET_CURRENT_USER = gql`
query {
  me {
    username
  }
}
`;

export const GET_MY_PROFILE = gql`
query GetMyProfile($userName: String!) {
  getUserProfile(userName: $userName) {
    id
    profileBio
    profilePic {
      id
      url
      feedUrl
      thumbnailUrl
    }
    coverPic {
      id
      url
      feedUrl
    }
    user {
      id
      username
      name
      email
    }
    city {
      id
      name
    }
  }
}
`;
