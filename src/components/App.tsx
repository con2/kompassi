import * as React from 'react';
import { Route, Switch } from 'react-router';
import { BrowserRouter as Router } from 'react-router-dom';

import CallbackView from './common/SessionContext/CallbackView';
import AccommodationOnboardingView from './accommodation/AccommodationOnboardingView';
import FormListView from './forms';
import FormEditorView from './forms/FormEditorView';
import FormView from './forms/FormView';

import FrontPage from './FrontPage';
import Navigation from './Navigation';
import NotFound from './NotFound';
import { SessionProvider } from './common/SessionContext';
import FormResponsesView from './forms/FormResponsesView';

class App extends React.Component {
  render() {
    return (
      <SessionProvider>
        <Router>
          <Navigation />
          <Switch>
            <Route exact={true} path="/" component={FrontPage} />
            <Route path="/events/:eventSlug/accommodation/onboarding" component={AccommodationOnboardingView} />
            <Route path="/forms/:slug(new)" component={FormEditorView} />
            <Route path="/forms/:slug/edit" component={FormEditorView} />
            <Route path="/forms/:slug/responses" component={FormResponsesView} />
            <Route path="/forms/:slug" component={FormView} />
            <Route path="/forms" component={FormListView} />
            <Route path="/oauth2/callback" component={CallbackView} />
            <Route component={NotFound} />
          </Switch>
        </Router>
      </SessionProvider>
    );
  }
}

export default App;
