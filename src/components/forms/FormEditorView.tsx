import React from "react";

import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";

import { dummyForm as form, FormSchema } from "./models";
import { propertiesFormFields } from "./propertiesForm";
import { SchemaForm, useSchemaForm } from "./SchemaForm";
import { T } from "../../translations";
import FormEditor from "./FormEditor";
import MainViewContainer from "../common/MainViewContainer";

const TabContent = ({ children }: { children?: React.ReactNode }) => (
  <div className="mt-3">{children}</div>
);

const FormEditorView = () => {
  const [fields, setFields] = React.useState(form.fields);
  const [properties, setProperties] = React.useState(form);
  const { title, layout } = properties;
  const t = T((r) => r.FormEditor);

  const previewSchemaForm = useSchemaForm(
    {
      fields,
      layout,
      showSubmitButton: false,
    },
    {}
  );
  const propertiesSchemaForm = useSchemaForm(
    {
      fields: propertiesFormFields,
      layout: "horizontal",
    },
    {
      initialValues: form,
      onSubmit: setProperties,
    }
  );

  return (
    <MainViewContainer>
      <h2>{title}</h2>
      <Tabs defaultActiveKey="design">
        <Tab eventKey="design" title={t((r) => r.Tabs.design)}>
          <TabContent>
            <FormEditor value={fields} onChange={setFields} />
          </TabContent>
        </Tab>
        <Tab eventKey="preview" title={t((r) => r.Tabs.preview)}>
          <TabContent>
            <SchemaForm {...previewSchemaForm} />
          </TabContent>
        </Tab>
        <Tab eventKey="properties" title={t((r) => r.Tabs.properties)}>
          <TabContent>
            <SchemaForm {...propertiesSchemaForm} />
          </TabContent>
        </Tab>
      </Tabs>
    </MainViewContainer>
  );
};

export default FormEditorView;
