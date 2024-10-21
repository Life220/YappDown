import svelte from 'rollup-plugin-svelte';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import { terser } from 'rollup-plugin-terser';
import sveltePreprocess from 'svelte-preprocess';

export default {
    input: '/YappDown/app/static/svelte/main.js',
    output: {
        sourcemap: true,
        format: 'iife',
        name: 'app',
        file: '/YappDown/app/static/build/bundle.js'
    },
    plugins: [
        svelte({
            preprocess: sveltePreprocess(),
            compilerOptions: {
                dev: !process.env.NODE_ENV === 'production'
            },
            emitCss: true
        }),
        resolve({
            browser: true,
            dedupe: ['svelte']
        }),
        commonjs(),
        process.env.NODE_ENV === 'production' && terser()
    ]
};