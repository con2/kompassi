import Container from "react-bootstrap/Container";
import { dummyForm, FormSchema } from "./models";

import SchemaForm from "./SchemaForm";

const FormView = () => (
  <Container>
    <h1>{dummyForm.title}</h1>
    <SchemaForm
      fields={dummyForm.fields}
      layout={dummyForm.layout}
      initialValues={{}}
      onSubmit={(values) => console.log(values)}
    />
  </Container>
);

export default FormView;
