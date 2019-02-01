import React from 'react';
import Spinner from 'reactstrap/lib/Spinner';

import { getWithCredentials } from './helpers';
import Session, { emptySession } from './Session';


const SessionContext = React.createContext<Session>(emptySession);
export const SessionConsumer = SessionContext.Consumer;


interface SessionProviderState {
  session?: Session;
}


export class SessionProvider extends React.Component<{}, SessionProviderState> {
  // why do I have to type this explicitly? :thinking:
  state: SessionProviderState = {
    session: undefined,
  };

  async componentDidMount() {
    if (window.location.hash) {
      // OAuth2 callback
      const hash = window.location.hash;
      window.location.hash = '';

      const user = await getWithCredentials('user', ''); // TODO this.state.token
      this.setState({ session: new Session(user) });
    } else {
      // Not logged in
      this.setState({ session: emptySession });
    }
  }

  render() {
    const { session } = this.state;

    if (session) {
      return (
        <SessionContext.Provider value={session}>
          {this.props.children}
        </SessionContext.Provider>
      );
    } else {
      return <Spinner />;
    }

  }
}


export default SessionContext;
