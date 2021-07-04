import assert from "assert";
import generateUniqueIdentifier from "./generateUniqueIdentifier";

describe(generateUniqueIdentifier, () => {
  it("works as intended", () => {
    const examples = [
      {
        base: "",
        used: [],
        expected: "field",
      },
      {
        base: "Sähköpostiosoite",
        used: ["sahkopostiosoite", "sahkopostiosoite-2"],
        expected: "sahkopostiosoite-3",
      },
    ];

    for (const example of examples) {
      const actual = generateUniqueIdentifier(example.base, example.used);
      assert.strictEqual(actual, example.expected);
    }
  });
});
