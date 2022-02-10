/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getTodo = /* GraphQL */ `
  query GetTodo($id: ID!) {
    getTodo(id: $id) {
      id
      name
      description
      createdAt
      updatedAt
    }
  }
`;
export const listTodos = /* GraphQL */ `
  query ListTodos(
    $filter: ModelTodoFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listTodos(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        name
        description
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
export const getRefillLocation = /* GraphQL */ `
  query GetRefillLocation($id: ID!) {
    getRefillLocation(id: $id) {
      id
      name
      description
      streetAddress
      city
      stateProvinceOrRegion
      zipCode
      countryCode
      createdAt
      updatedAt
    }
  }
`;
export const listRefillLocations = /* GraphQL */ `
  query ListRefillLocations(
    $filter: ModelRefillLocationFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listRefillLocations(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        name
        description
        streetAddress
        city
        stateProvinceOrRegion
        zipCode
        countryCode
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
