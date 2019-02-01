import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { I18nextProvider } from 'react-i18next';
import { BrowserRouter as Router } from 'react-router-dom';

import App from './components/App';
import registerServiceWorker from './registerServiceWorker';
import i18n from './translations';

import 'bootstrap/dist/css/bootstrap.min.css';
import { SessionProvider } from './components/SessionContext';


ReactDOM.render(
  (
    <I18nextProvider i18n={i18n}>
      <SessionProvider>
        <Router>
          <App />
        </Router>
      </SessionProvider>
    </I18nextProvider>
  ),
  document.getElementById('root') as HTMLElement
);
registerServiceWorker();
