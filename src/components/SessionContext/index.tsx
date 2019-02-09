import React from 'react';
import Spinner from 'reactstrap/lib/Spinner';

import { getOAuth2, getWithCredentials } from './helpers';
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
    try {
      const token = await getOAuth2().token.getToken(window.location.href);
      const user = await getWithCredentials('user', token.accessToken);
      this.setState({ session: new Session(user, token) });
    } catch (e) {
      console.warn('Not logged in:', e);
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
