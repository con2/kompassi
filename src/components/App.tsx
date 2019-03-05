import * as React from 'react';
import { Route, Switch } from 'react-router';

import FormEditorView from './FormEditorView';
import FormListView from './FormListView';
import FormView from './FormView';
import FrontPage from './FrontPage';
import Navigation from './Navigation';
import NotFound from './NotFound';
import CallbackView from './SessionContext/CallbackView';



class App extends React.Component {
  render() {
    return (
      <div className='Application'>
        <Navigation />
        <Switch>
          <Route exact={true} path="/" component={FrontPage} />
          <Route path="/forms/:slug(new)" component={FormEditorView} />
          <Route path="/forms/:slug/edit" component={FormEditorView} />
          <Route path="/forms/:slug" component={FormView} />
          <Route path="/forms" component={FormListView} />
          <Route path="/oauth2/callback" component={CallbackView} />
          <Route component={NotFound} />
        </Switch>
      </div>
    );
  }
}

export default App;
