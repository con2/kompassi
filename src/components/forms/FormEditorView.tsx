import React from "react";

import { dummyForm } from "./models";
import MainViewContainer from "../common/MainViewContainer";

import FormEditor from "./FormEditor";

const FormEditorView = () => {
  const [value, setValue] = React.useState(dummyForm);

  return (
    <MainViewContainer>
      <FormEditor value={value} onChange={setValue} />
    </MainViewContainer>
  );
};

export default FormEditorView;
