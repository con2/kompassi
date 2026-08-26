import { SignInRequired } from "@con2/components";
import {
  Button,
  Card,
  CardBody,
  CardText,
  CardTitle,
  Container,
  Table,
} from "react-bootstrap";

import { CBAC_SUDO_CLAIM_KEYS } from "@/apolloClient";
import { auth } from "@/auth";
import isSiteRelativePath from "@/helpers/isSiteRelativePath";
import { getTranslations } from "@/translations";
import { sudoCbac } from "./actions";

interface Props {
  params: Promise<{
    locale: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export default async function SudoPage(props: Props) {
  const searchParams = await props.searchParams;
  const { locale } = await props.params;
  const translations = getTranslations(locale);
  const t = translations.Sudo;

  // TODO encap
  const session = await auth();
  if (!session) {
    return (
      <SignInRequired
        messages={translations.SignInRequired}
        providerId="kompassi"
        locale={locale}
      />
    );
  }

  const next =
    searchParams.next && isSiteRelativePath(searchParams.next)
      ? searchParams.next
      : "/";

  const claims: Record<string, string> = {};
  for (const key of CBAC_SUDO_CLAIM_KEYS) {
    const value = searchParams[key];
    if (value) {
      claims[key] = value;
    }
  }

  const confirm = sudoCbac.bind(null, next, claims);

  return (
    <Container>
      <Card>
        <CardBody>
          <CardTitle>{t.title}</CardTitle>
          <CardText>{t.warning}</CardText>

          <Table striped bordered className="mb-4">
            <thead>
              <tr>
                <th>{t.claimHeading}</th>
                <th>{t.valueHeading}</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(claims).map(([key, value]) => (
                <tr key={key}>
                  <td>
                    <code>{key}</code>
                  </td>
                  <td>
                    <code>{value}</code>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>

          <form action={confirm}>
            <Button type="submit" variant="danger">
              {t.confirm}
            </Button>
          </form>
        </CardBody>
      </Card>
    </Container>
  );
}
