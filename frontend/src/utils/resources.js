export const Race = {
  url: `${window.BACKEND_HOST}/races/api/race/<slug>`,
  async get(slug) {
    const url = this.url.replace('<slug>', encodeURIComponent(slug));
    const respoose = await fetch(url);
    return respoose.json();
  },
};


export const Qualification = {
  url: `${window.BACKEND_HOST}/races/api/race/<slug>/qualification`,
  async get(slug) {
    const url = this.url.replace('<slug>', encodeURIComponent(slug));
    const respoose = await fetch(url);
    return respoose.json();
  },
};


export const Brackets = {
  url: `${window.BACKEND_HOST}/races/api/race/<slug>/brackets/<type>/`,
  async get(slug, type) {
    const url = this.url.replace('<slug>', encodeURIComponent(slug)).replace('<type>', encodeURIComponent(type));
    const respoose = await fetch(url);
    return respoose.json();
  },
};
