import { mkdir, readFile, readdir, writeFile } from 'node:fs/promises'
import { dirname, join, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const appRoot = resolve(here, '..')
const repoRoot = resolve(appRoot, '..')
const runsRoot = join(repoRoot, 'runs')
const publicRoot = join(appRoot, 'public', 'data')
const entries = []

async function walk(dir) {
  for (const item of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, item.name)
    if (item.isDirectory()) await walk(path)
    if (item.isFile() && item.name === 'stdout.log') {
      const parts = relative(runsRoot, path).split(/[\\/]/)
      const [runId, , task, harness, repetition] = parts
      const metadataPath = join(dirname(path), 'metadata.json')
      const metadata = JSON.parse(await readFile(metadataPath, 'utf8'))
      const target = join(publicRoot, 'logs', runId, task, harness, repetition, 'stdout.log')
      await mkdir(dirname(target), { recursive: true })
      const taskStatement = (await readFile(join(repoRoot, 'tasks', task, 'task.md'), 'utf8')).replace(/\r\n/g, '\n').trim()
      const encodedStatement = JSON.stringify(taskStatement).slice(1, -1)
      const rawLog = await readFile(path, 'utf8')
      const redaction = '[texto literal do enunciado removido para o experimento]'
      const sanitizedLog = rawLog
        .replaceAll(taskStatement, redaction)
        .replaceAll(encodedStatement, redaction)
        .replace(/\u001b\[[0-9;]*m/g, '')
      await writeFile(target, sanitizedLog)
      entries.push({
        id: `${runId}:${task}:${harness}:${repetition}`,
        runId, task, harness, repetition,
        url: `/data/logs/${runId}/${task}/${harness}/${repetition}/stdout.log`,
        elapsedSeconds: metadata.elapsed_seconds,
        status: metadata.status,
        model: metadata.model,
      })
    }
  }
}

await mkdir(publicRoot, { recursive: true })
await walk(runsRoot)
entries.sort((a, b) => a.id.localeCompare(b.id))
await writeFile(join(publicRoot, 'manifest.json'), JSON.stringify({ generatedAt: new Date().toISOString(), entries }, null, 2))
console.log(`Prepared ${entries.length} traces in public/data.`)
