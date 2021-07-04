import renderer from "react-test-renderer";

import { dummyForm } from "./models";
import SchemaForm, { useSchemaForm } from "./SchemaForm";

function DummyFormTest() {
  const schemaForm = useSchemaForm(dummyForm);
  return <SchemaForm {...schemaForm} />;
}

describe(SchemaForm, () => {
  it("renders the dummy form", () => {
    const component = renderer.create(<DummyFormTest />);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
