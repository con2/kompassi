import Container from "react-bootstrap/Container";
import { dummyForm, FormSchema } from "./models";

import SchemaForm from "./SchemaForm";

const FormView = () => (
  <Container>
    <h1>{dummyForm.title}</h1>
    <SchemaForm
      schema={dummyForm}
      initialValues={{}}
      onSubmit={(values) => console.log(values)}
    />
  </Container>
);

export default FormView;
