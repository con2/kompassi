interface Config {
  api: {
    baseUrl: string;
    clientId: string;
  };
}

const Config: Config = {
  api: {
    baseUrl: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v3',
    clientId: 'insecure kompassi v2 development client id',
  },
};

export default Config;
