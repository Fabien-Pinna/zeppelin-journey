/** Resolve public assets and navigation under either host's deployment base. */
export const assetUrl = (path = '') => `${import.meta.env.BASE_URL}${path.replace(/^\/+/, '')}`;
