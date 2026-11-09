import { openDatabase, migrate } from '../database.mjs'
import { createApiHandler } from '../server.mjs'

let initialization
export default async function api(request, response) {
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
