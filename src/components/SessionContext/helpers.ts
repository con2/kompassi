import Config from '../../Config';


export async function getWithCredentials(path: string, token: string) {
  const url = `${Config.api.baseUrl}/${path}`;
  const headers: { [name: string]: string; } = {
    accept: 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, { headers });
  return response.json();
}
