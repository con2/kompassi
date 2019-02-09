import ClientOAuth2 from 'client-oauth2';

import Config from '../../Config';


export async function getWithCredentials(path: string, token: string) {
  const url = `${Config.api.baseUrl}/api/v3/${path}`;
  const headers: { [name: string]: string; } = {
    accept: 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, { headers });
  return response.json();
}


export function getOAuth2() {
  return new ClientOAuth2({
    clientId: Config.api.clientId,
    accessTokenUri: `${Config.api.baseUrl}/oauth2/token`,
    authorizationUri: `${Config.api.baseUrl}/oauth2/authorize`,
    // TODO: add ?next=${window.location.href} urlencoded
    redirectUri: `${Config.publicUrl}/oauth2/callback`,
    scopes: ['read', 'write']
  });
}
