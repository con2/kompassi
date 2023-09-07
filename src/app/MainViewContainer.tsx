import React, { ReactNode } from "react";

import { t } from "../translations";

import "./MainViewContainer.scss";

interface MainViewContainerProps {
  loading?: boolean;
  error?: any;
  children?: ReactNode;
}

const MainViewContainer: React.FC<MainViewContainerProps> = ({
  loading,
  error,
  children,
}) => {
  if (error) {
    return (
      <div className="container MainViewContainer">
        <div className="alert alert-danger">
          {error
            ? error.message || t((r) => r.MainView.defaultErrorMessage)
            : t((r) => r.MainView.defaultErrorMessage)}
        </div>
      </div>
    );
  } else if (loading) {
    return (
      <div className="container MainViewContainer">
        <p>Loading…</p>
      </div>
    );
  } else {
    return <div className="container MainViewContainer">{children}</div>;
  }
};

export default MainViewContainer;
