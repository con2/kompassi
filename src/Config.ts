interface Config {
  publicUrl: string;
  api: {
    baseUrl: string;
    clientId: string;
  };
}

const Config: Config = {
  publicUrl: process.env.PUBLIC_URL || 'http://localhost:3000',
  api: {
    baseUrl: process.env.REACT_APP_KOMPASSI_BASE_URL || 'http://localhost:8000',
    clientId: process.env.REACT_APP_CLIENT_ID || 'insecure kompassi v2 development client id',
  },
};

export default Config;
