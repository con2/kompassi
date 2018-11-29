import * as React from 'react';
import { Route, Switch } from 'react-router';

import FormView from './FormView';
import FrontPage from './FrontPage';
import Navigation from './Navigation';
import NotFound from './NotFound';


class App extends React.Component {
  render() {
    return (
      <div className='Application'>
        <Navigation />
        <Switch>
          <Route exact={true} path="/" render={FrontPage} />
          <Route path="/forms/:formSlug" render={() => <FormView />} />
          <Route render={NotFound} />
        </Switch>
      </div>
    );
  }
}

export default App;
