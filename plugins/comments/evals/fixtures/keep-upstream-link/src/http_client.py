def fetch(session, url):
    # requests 2.31 drops the Authorization header when a redirect changes the host,
    # so follow redirects by hand. https://github.com/psf/requests/issues/6377
    resp = session.get(url, allow_redirects=False)
    while resp.is_redirect:
        resp = session.get(resp.headers["Location"], allow_redirects=False)
    return resp
