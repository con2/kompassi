import Navigation from "./Navigation";
import FormEditorView from "./forms/FormEditorView";

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import SplashView from "./SplashView";
import MainViewContainer from "./common/MainViewContainer";
import EventsView from "./events/EventsView";

const router = createBrowserRouter([
  {
    path: "/",
    children: [
      {
        path: "forms",
        element: <FormEditorView />,
      },
      {
        path: "events",
        element: <EventsView />,
      },
      {
        path: "",
        element: <SplashView />,
      },
    ],
    errorElement: <MainViewContainer error={true} />,
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
