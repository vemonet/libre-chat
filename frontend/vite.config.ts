import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [sveltekit()],
	// build: {
	// 	emptyOutDir: true,
	// 	outDir: '../src/libre_chat/webapp',
	// 	outDir: '../public',
	// 	assetsDir: 'assets',
	// 	rollupOptions: {
	// 		 input: {
	// 				main: './index.html',
	// 				example: './pages/example.html',
	// 		 },
	// 		 output: {
	// 				entryFileNames: 'assets/js/[name]-[hash].js',
	// 				chunkFileNames: 'assets/js/[name]-[hash].js',
	// 				assetFileNames: ({ name }) => {
	// 					 if (/\.(gif|jpe?g|png|svg)$/.test(name ?? '')) {
	// 							return 'assets/images/[name].[ext]';
	// 					 }

	// 					 if (/\.css$/.test(name ?? '')) {
	// 							return 'assets/css/[name]-[hash].[ext]';
	// 					 }

	// 					 return 'assets/[name]-[hash].[ext]';
	// 				},
	// 		 }
	// 	}
 	// },
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
});
