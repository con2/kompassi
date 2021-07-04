import renderer from "react-test-renderer";

import { dummyForm } from "./models";
import SchemaForm from "./SchemaForm";

describe(SchemaForm, () => {
  it("renders the dummy form", () => {
    const component = renderer.create(
      <SchemaForm
        fields={dummyForm.fields}
        layout={dummyForm.layout}
        onSubmit={(values) => console.log(values)}
      />
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
