import React from 'react';
import { useParams } from 'react-router-dom';
import useSWR from 'swr';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import Alert from 'reactstrap/lib/Alert';

import { Form } from './SchemaForm/models';
import { Spinner } from 'reactstrap';
import { T } from '../../translations';
import MainViewContainer from '../common/MainViewContainer';
import SchemaForm from './SchemaForm';
import SessionContext from '../common/SessionContext';

const FormView: React.FC<{}> = () => {
  const { slug } = useParams();
  const context = React.useContext(SessionContext);
  const { error, data } = useSWR<Form>(`forms/${slug}`, context.get);
  const t = T(r => r.Common);
  const [value, setValue] = React.useState({});
  const [postError, setPostError] = React.useState<Error | null>(null);
  const [posting, setPosting] = React.useState(false);

  const onSubmit = React.useCallback(
    (values: any) => {
      (async function() {
        try {
          setPosting(true);
          await context.post(`forms/${slug}/responses`, { values });
        } catch (err) {
          setPostError(err);
        } finally {
          setPosting(false);
        }
      })();
    },
    [slug, context],
  );

  if (error || !data) {
    return <MainViewContainer error={error} loading={!data} />;
  }

  const { title, layout, fields } = data;

  return (
    <MainViewContainer>
      {title && <h1>{title}</h1>}
      <SchemaForm fields={fields} layout={layout} value={value} onChange={setValue} onSubmit={onSubmit} readOnly={posting}>
        <ButtonGroup className="mt-2">
          <Button color="primary" type="submit" disabled={posting}>
            {t(r => r.submit)}
            {posting && <Spinner size="sm" color="light" className="ml-1" />}
          </Button>
        </ButtonGroup>
      </SchemaForm>
      {postError && (
        <Alert className="mt-3" color="danger">
          {postError.message || t(r => r.somethingWentWrong)}
        </Alert>
      )}
    </MainViewContainer>
  );
};

export default FormView;
