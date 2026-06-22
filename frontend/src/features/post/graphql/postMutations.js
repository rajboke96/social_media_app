import { gql } from '@apollo/client';

export const CREATE_POST_MUTATION = gql`
mutation CreatePost($data: UserPostInput!) {
  createPost(data: $data) {
    id
    title
    description
    visibility
    createdBy {
      username
      name
      id
    }
  }
}
`;

export const UPDATE_POST_MUTATION = gql`
mutation UpdatePost($data: UpdatePostInput!) {
  updatePost(data: $data) {
    id
    title
    description
    visibility
  }
}
`;

export const DELETE_POST_MUTATION = gql`
mutation DeletePost($postId: Int!) {
  deletePost(postId: $postId)
}
`;
