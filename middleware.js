export default async function middleware(request) {
  const url = new URL(request.url);
  if (url.pathname !== '/') return;

  const lang = request.headers.get('accept-language') || '';
  const target = lang.startsWith('uk') ? '/index-ua.html' : '/index.html';

  return fetch(new URL(target, request.url));
}

export const config = {
  matcher: '/'
};
