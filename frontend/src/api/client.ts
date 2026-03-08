export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      ...(init?.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
      ...init?.headers,
    },
    ...init,
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(payload.detail ?? 'Request failed')
  }

  const contentType = response.headers.get('content-type') ?? ''
  if (contentType.includes('application/json')) {
    return response.json() as Promise<T>
  }
  return response.blob() as T
}
