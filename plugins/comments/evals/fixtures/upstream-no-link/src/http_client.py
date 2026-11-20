def fetch_head(session, url):
    resp = session.get(url, stream=True)
    first = resp.raw.read(1024)
    # urllib3 has a bug: closing a streamed response before it is read to the end
    # leaks the pooled connection, so drain the rest of the body before closing.
    for _ in resp.iter_content(65536):
        pass
    resp.close()
    return first
