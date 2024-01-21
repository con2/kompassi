import { CodegenConfig } from "@graphql-codegen/cli";

import { kompassiBaseUrl } from "./src/config";

const config: CodegenConfig = {
  schema: `${kompassiBaseUrl}/graphql`,
  documents: ["src/**/*.{ts,tsx}"],
  generates: {
    "./src/__generated__/": {
      preset: "client",
      plugins: [],
      presetConfig: {
        gqlTagName: "graphql",
        fragmentMasking: false,
      },
    },
  },
  ignoreNoDocuments: true,
  config: {
    scalars: {
      DateTime: "string",
      GenericScalar: "unknown",
      JSONString: "string",
      UUID: "string",
    },
  },
};

export default config;
