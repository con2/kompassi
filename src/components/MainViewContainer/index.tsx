import React from 'react';

import Container from "reactstrap/lib/Container";

import './index.css';


export default class MainViewContainer extends React.Component<{}, {}> {
  render() {
    return <Container className='MainViewContainer'>{this.props.children}</Container>;
  }
}
