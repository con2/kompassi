import renderer from "react-test-renderer";
import { dummyForm } from "./models";

import FormEditor from "./FormEditor";

describe(FormEditor, () => {
  it("renders the dummy form", () => {
    const component = renderer.create(
      <FormEditor value={dummyForm} onChange={() => {}} />
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
