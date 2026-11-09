import { openDatabase, migrate } from '../database.mjs'
import { createApiHandler } from '../server.mjs'

let initialization
export default async function api(request, response) {
  // Vercel forwards nested API paths to this single Function through a rewrite.
  const route = request.query?.route ?? new URL(request.url, 'http://localhost').searchParams.get('route')
  if (typeof route === 'string') request.url = `/api/${route}`
  initialization ??= openDatabase().then(async (database) => {
    try {
      await migrate(database)
      return createApiHandler({ database })
    } catch (error) {
      database.close()
      throw error
    }
  }).catch((error) => {
    initialization = undefined
    throw error
  })
  return (await initialization)(request, response)
}
