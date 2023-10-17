import React, { ReactNode } from "react";

import type { Translations } from "@/translations/en";

import "./MainViewContainer.scss";


interface MainViewContainerProps {
  loading?: boolean;
  error?: any;
  children?: ReactNode;
  translations: Translations;
}

const MainViewContainer: React.FC<MainViewContainerProps> = ({
  loading,
  error,
  children,
  translations,
}) => {
  if (error) {
    return (
      <div className="container MainViewContainer">
        <div className="alert alert-danger">
          {error
            ? error.message || translations.MainView.defaultErrorMessage
            : translations.MainView.defaultErrorMessage}
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
