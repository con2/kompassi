import Navigation from "./Navigation";
import FormEditorView from "./forms/FormEditorView";

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import SplashView from "./SplashView";
import MainViewContainer from "./common/MainViewContainer";
import EventsView from "./EventsView";

const router = createBrowserRouter([
  {
    path: "/",
    element: <SplashView />,
  },
  {
    path: "/forms",
    element: <FormEditorView />,
  },
  {
    path: "/events",
    element: <EventsView />,
  },
]);

function App() {
  return (
    <div>
      <Navigation />
      <MainViewContainer>
        <RouterProvider router={router} />
      </MainViewContainer>
    </div>
  );
}

export default App;
