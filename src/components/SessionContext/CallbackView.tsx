import React from 'react';
import { Redirect } from 'react-router-dom';


interface CallbackViewState {
  next: string;
}


export default class CallbackView extends React.Component<{}, CallbackViewState> {
  state = {
    next: '/',
  };

  componentDidMount() {
    // TODO: parse ?next=
  }

  render() {
    const { next } = this.state;
    return <Redirect to={next} />;
  }
}
