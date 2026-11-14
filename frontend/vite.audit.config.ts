// Isolated production-preview proxy for the audit; normal dev/hosting config is unchanged.
import { mergeConfig } from 'vite'
import base from './vite.config'

export default mergeConfig(base, {
  preview: { proxy: { '/api': { target: 'http://127.0.0.1:8019' } } },
})
