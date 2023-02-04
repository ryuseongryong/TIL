import React, { useEffect, useReducer } from 'react';
import Amplify from '@aws-amplify/core';
import { API, graphqlOperation } from 'aws-amplify';
import { createTodo } from './graphql/mutations';
import { listTodos } from './graphql/queries';
import { onCreateTodo, onUpdateTodo } from './graphql/subscriptions';

import config from './aws-exports';
Amplify.configure(config); // Configure Amplify

const initialState = { todos: [] };
const reducer = (state, action) => {
  switch (action.type) {
    case 'QUERY':
      return { ...state, todos: action.todos };
    case 'SUBSCRIPTION':
      return { ...state, todos: [...state.todos, action.todo] };
    default:
      return state;
  }
};

async function createNewTodo() {
  const todo = { name: 'Use AppSync', description: 'Realtime and Offline' };
  await API.graphql(graphqlOperation(createTodo, { input: todo }));
}
function App() {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    getData();
    const subscription = API.graphql(graphqlOperation(onCreateTodo)).subscribe({
      next: (eventData) => {
        const todo = eventData.value.data.onCreateTodo;
        dispatch({ type: 'SUBSCRIPTION', todo });
      },
    });
    return () => {
      subscription.unsubscribe();
    };
  }, []);

  async function getData() {
    const todoData = await API.graphql(graphqlOperation(listTodos));
    dispatch({ type: 'QUERY', todos: todoData.data.listTodos.items });
  }

  return (
    <div>
      <div className="App">
        <button onClick={createNewTodo}>Add Todo</button>
      </div>
      <div>
        {state.todos.map((todo, i) => (
          <p key={todo.id}>
            {todo.name} : {todo.description}
          </p>
        ))}
      </div>
    </div>
  );
}
export default App;
