/* eslint-disable import/prefer-default-export */
export const SensorSignal = {
  url: `${window.BACKEND_HOST}/api/sensors/signal`,
  async post(data) {
    const respoose = await fetch(this.url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json;charset=utf-8' },
      body: JSON.stringify(data),
    });
    return respoose.json();
  },
};
