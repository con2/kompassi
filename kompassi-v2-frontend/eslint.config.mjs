import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import prettier from "eslint-config-prettier";
import tseslint from "typescript-eslint";

const eslintConfig = [
  ...nextCoreWebVitals,
  prettier,
  {
    ignores: ["src/__generated__/*.ts"],
  },
  {
    files: ["**/*.ts", "**/*.tsx"],
    plugins: { "@typescript-eslint": tseslint.plugin },
    rules: {
      "@typescript-eslint/no-explicit-any": "off",
      "@typescript-eslint/no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_" },
      ],
    },
  },
];

export default eslintConfig;
