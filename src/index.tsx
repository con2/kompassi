import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';

import App from './components/App';
import './translations';

import 'bootstrap/dist/css/bootstrap.min.css';
import { SessionProvider } from './components/common/SessionContext';

ReactDOM.render(
  <SessionProvider>
    <Router>
      <App />
    </Router>
  </SessionProvider>,
  document.getElementById('root') as HTMLElement,
);
