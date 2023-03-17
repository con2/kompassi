import Navigation from "./Navigation";
import FormEditorView from "./forms/FormEditorView";

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import SplashView from "./SplashView";
import MainViewContainer from "./common/MainViewContainer";

const router = createBrowserRouter([
  {
    path: "/",
    element: <SplashView />,
  },
  {
    path: "/forms",
    element: <FormEditorView />,
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
