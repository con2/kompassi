import React from 'react';

import Alert from 'reactstrap/lib/Alert';
import Container from 'reactstrap/lib/Container';

import Loading from '../Loading';

import './index.css';
import { t } from '../../../translations';

interface MainViewContainerProps {
  loading?: boolean;
  error?: any;
}

const MainViewContainer: React.FC<MainViewContainerProps> = ({ loading, error, children }) => {
  if (error) {
    return (
      <Container className="MainViewContainer">
        <Alert color="danger">
          {error ? error.message || t(r => r.MainView.defaultErrorMessage) : t(r => r.MainView.defaultErrorMessage)}
        </Alert>
      </Container>
    );
  } else if (loading) {
    return (
      <Container className="MainViewContainer">
        <Loading />
      </Container>
    );
  } else {
    return <Container className="MainViewContainer">{children}</Container>;
  }
};

export default MainViewContainer;
