import Container from "react-bootstrap/Container";
import { dummyForm, FormSchema } from "./models";

import SchemaForm, { useSchemaForm } from "./SchemaForm";

const FormView = () => {
  const schemaForm = useSchemaForm(dummyForm, {
    onSubmit(values) {
      console.log(values);
    },
  });
  return (
    <Container>
      <h1>{dummyForm.title}</h1>
      <SchemaForm {...schemaForm} />
    </Container>
  );
};

export default FormView;
