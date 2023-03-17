import React, { ReactNode } from "react";

import Alert from "react-bootstrap/Alert";
import Container from "react-bootstrap/Container";

import Loading from "./Loading";
import { t } from "../../translations";

import "./MainViewContainer.scss";

interface MainViewContainerProps {
  loading?: boolean;
  error?: any;
  children: ReactNode;
}

const MainViewContainer: React.FC<MainViewContainerProps> = ({
  loading,
  error,
  children,
}) => {
  if (error) {
    return (
      <Container className="MainViewContainer">
        <Alert color="danger">
          {error
            ? error.message || t((r) => r.MainView.defaultErrorMessage)
            : t((r) => r.MainView.defaultErrorMessage)}
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
