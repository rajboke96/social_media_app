import { gql } from '@apollo/client';

export const LOGIN_MUTATION = gql`
mutation Login($data: CreateTokenInput!) {
  login(data: $data)
}
`;

export const SIGNUP_MUTATION = gql`
mutation Signup($data: CreateUserInput!) {
  signup(data: $data)
}
`;

export const ME_QUERY = gql`
query Me {
  me {
    username
    role
  }
}
`;

export const LOGOUT_MUTATION = gql`
mutation Logout {
  logout
}
`;
