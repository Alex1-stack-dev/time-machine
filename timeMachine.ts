export const timeMachineConfig = {
  apiUrl: process.env.NEXT_PUBLIC_TIME_MACHINE_API_URL || 'https://time-machine-kjr4.vercel.app',
  apiKey: process.env.NEXT_PUBLIC_TIME_MACHINE_API_KEY || '',
  refreshInterval: 1000, // 1 second refresh rate
  retryAttempts: 3,
  retryDelay: 5000, // 5 seconds between retries
  endpoints: {
    connect: '/api/connect',
    results: '/api/results',
    splits: '/api/splits',
    live: '/api/live',
  }
};
