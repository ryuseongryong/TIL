/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const createTodo = /* GraphQL */ `
  mutation CreateTodo(
    $input: CreateTodoInput!
    $condition: ModelTodoConditionInput
  ) {
    createTodo(input: $input, condition: $condition) {
      id
      name
      description
      createdAt
      updatedAt
    }
  }
`;
export const updateTodo = /* GraphQL */ `
  mutation UpdateTodo(
    $input: UpdateTodoInput!
    $condition: ModelTodoConditionInput
  ) {
    updateTodo(input: $input, condition: $condition) {
      id
      name
      description
      createdAt
      updatedAt
    }
  }
`;
export const deleteTodo = /* GraphQL */ `
  mutation DeleteTodo(
    $input: DeleteTodoInput!
    $condition: ModelTodoConditionInput
  ) {
    deleteTodo(input: $input, condition: $condition) {
      id
      name
      description
      createdAt
      updatedAt
    }
  }
`;
export const createRefillLocation = /* GraphQL */ `
  mutation CreateRefillLocation(
    $input: CreateRefillLocationInput!
    $condition: ModelRefillLocationConditionInput
  ) {
    createRefillLocation(input: $input, condition: $condition) {
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
export const updateRefillLocation = /* GraphQL */ `
  mutation UpdateRefillLocation(
    $input: UpdateRefillLocationInput!
    $condition: ModelRefillLocationConditionInput
  ) {
    updateRefillLocation(input: $input, condition: $condition) {
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
export const deleteRefillLocation = /* GraphQL */ `
  mutation DeleteRefillLocation(
    $input: DeleteRefillLocationInput!
    $condition: ModelRefillLocationConditionInput
  ) {
    deleteRefillLocation(input: $input, condition: $condition) {
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
