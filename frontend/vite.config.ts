import {defineConfig, loadEnv} from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig(({mode})=>({define:{__BACKEND_URL__:JSON.stringify(loadEnv(mode,process.cwd(),'VITE_').VITE_BACKEND_URL||''),__APP_TOKEN__:JSON.stringify(loadEnv(mode,process.cwd(),'VITE_').VITE_APP_TOKEN||'')},plugins:[react()],root:'frontend',build:{outDir:'../dist-local',emptyOutDir:true}}));
