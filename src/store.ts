import { routerMiddleware } from 'connected-react-router';
import { createBrowserHistory } from 'history';
import { applyMiddleware, compose, createStore } from 'redux';

import createRootReducer from './modules';


export const history = createBrowserHistory();

export default createStore(
  createRootReducer(history),
  compose(
    applyMiddleware(
      routerMiddleware(history),
    ),
  ),
);
