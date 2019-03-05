import React from 'react';
import { Redirect } from 'react-router-dom';
import Spinner from 'reactstrap/lib/Spinner';


interface CallbackViewState {
  next: string | null;
}


export default class CallbackView extends React.Component<{}, CallbackViewState> {
  state = {
    next: null,
  };

  componentDidMount() {
    if (window.location.search) {
      const params = new URLSearchParams(window.location.search);
      const next = params.get('next');
      if (next) {
        this.setState({ next });
      }
    } else {
      this.setState({ next: '/' });
    }
  }

  render() {
    const { next } = this.state;
    if (next) {
      return <Redirect to={next} />;
    } else {
      return <Spinner />;
    }
  }
}
