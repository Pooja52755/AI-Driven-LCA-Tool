
import root from '../root.svelte';
import { set_building } from '__sveltekit/environment';
import { set_assets } from '__sveltekit/paths';
import { set_private_env, set_public_env } from '../../../node_modules/@sveltejs/kit/src/runtime/shared-server.js';

export const options = {
	app_template_contains_nonce: false,
	csp: {"mode":"auto","directives":{"upgrade-insecure-requests":false,"block-all-mixed-content":false},"reportOnly":{"upgrade-insecure-requests":false,"block-all-mixed-content":false}},
	csrf_check_origin: true,
	track_server_fetches: false,
	embedded: false,
	env_public_prefix: 'PUBLIC_',
	env_private_prefix: '',
	hooks: null, // added lazily, via `get_hooks`
	preload_strategy: "modulepreload",
	root,
	service_worker: false,
	templates: {
		app: ({ head, body, assets, nonce, env }) => "<!DOCTYPE html>\r\n<html lang=\"en\">\r\n\t<head>\r\n\t\t<meta charset=\"utf-8\" />\r\n\t\t<link rel=\"icon\" href=\"" + assets + "/favicon.png\" />\r\n\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\r\n\t\t<title>AI-Driven LCA Tool for Metallurgy - SIH 2025</title>\r\n\t\t<meta name=\"description\" content=\"Advanced Life Cycle Assessment platform for metals and mining with AI-powered circularity analysis\" />\r\n\t\t\r\n\t\t<!-- Tailwind CSS -->\r\n\t\t<script src=\"https://cdn.tailwindcss.com\"></script>\r\n\t\t\r\n\t\t<!-- Chart.js -->\r\n\t\t<script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>\r\n\t\t\r\n\t\t<!-- Vis.js -->\r\n\t\t<script src=\"https://unpkg.com/vis-network/standalone/umd/vis-network.min.js\"></script>\r\n\t\t\r\n\t\t<style>\r\n\t\t\t:root {\r\n\t\t\t\t--primary-color: #0f766e;\r\n\t\t\t\t--secondary-color: #06b6d4;\r\n\t\t\t\t--accent-color: #f59e0b;\r\n\t\t\t\t--success-color: #10b981;\r\n\t\t\t\t--warning-color: #f59e0b;\r\n\t\t\t\t--error-color: #ef4444;\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\tbody {\r\n\t\t\t\tfont-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;\r\n\t\t\t\tbackground: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t.glass-morphism {\r\n\t\t\t\tbackground: rgba(255, 255, 255, 0.25);\r\n\t\t\t\tbackdrop-filter: blur(10px);\r\n\t\t\t\tborder: 1px solid rgba(255, 255, 255, 0.18);\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t.gradient-bg {\r\n\t\t\t\tbackground: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t.chart-container {\r\n\t\t\t\tposition: relative;\r\n\t\t\t\theight: 400px;\r\n\t\t\t\twidth: 100%;\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t.vis-network {\r\n\t\t\t\theight: 500px;\r\n\t\t\t\tborder: 1px solid #e5e7eb;\r\n\t\t\t\tborder-radius: 0.5rem;\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t.metric-card {\r\n\t\t\t\ttransition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t.metric-card:hover {\r\n\t\t\t\ttransform: translateY(-2px);\r\n\t\t\t\tbox-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t.tab-active {\r\n\t\t\t\tbackground: var(--primary-color);\r\n\t\t\t\tcolor: white;\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t.loading-spinner {\r\n\t\t\t\tborder: 3px solid #f3f3f3;\r\n\t\t\t\tborder-top: 3px solid var(--primary-color);\r\n\t\t\t\tborder-radius: 50%;\r\n\t\t\t\twidth: 24px;\r\n\t\t\t\theight: 24px;\r\n\t\t\t\tanimation: spin 1s linear infinite;\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t@keyframes spin {\r\n\t\t\t\t0% { transform: rotate(0deg); }\r\n\t\t\t\t100% { transform: rotate(360deg); }\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t.fade-in {\r\n\t\t\t\tanimation: fadeIn 0.5s ease-in-out;\r\n\t\t\t}\r\n\t\t\t\r\n\t\t\t@keyframes fadeIn {\r\n\t\t\t\tfrom { opacity: 0; transform: translateY(20px); }\r\n\t\t\t\tto { opacity: 1; transform: translateY(0); }\r\n\t\t\t}\r\n\t\t</style>\r\n\t\t\r\n\t\t" + head + "\r\n\t</head>\r\n\t<body data-sveltekit-preload-data=\"hover\" class=\"min-h-screen\">\r\n\t\t<div style=\"display: contents\">" + body + "</div>\r\n\t</body>\r\n</html>",
		error: ({ status, message }) => "<!doctype html>\n<html lang=\"en\">\n\t<head>\n\t\t<meta charset=\"utf-8\" />\n\t\t<title>" + message + "</title>\n\n\t\t<style>\n\t\t\tbody {\n\t\t\t\t--bg: white;\n\t\t\t\t--fg: #222;\n\t\t\t\t--divider: #ccc;\n\t\t\t\tbackground: var(--bg);\n\t\t\t\tcolor: var(--fg);\n\t\t\t\tfont-family:\n\t\t\t\t\tsystem-ui,\n\t\t\t\t\t-apple-system,\n\t\t\t\t\tBlinkMacSystemFont,\n\t\t\t\t\t'Segoe UI',\n\t\t\t\t\tRoboto,\n\t\t\t\t\tOxygen,\n\t\t\t\t\tUbuntu,\n\t\t\t\t\tCantarell,\n\t\t\t\t\t'Open Sans',\n\t\t\t\t\t'Helvetica Neue',\n\t\t\t\t\tsans-serif;\n\t\t\t\tdisplay: flex;\n\t\t\t\talign-items: center;\n\t\t\t\tjustify-content: center;\n\t\t\t\theight: 100vh;\n\t\t\t\tmargin: 0;\n\t\t\t}\n\n\t\t\t.error {\n\t\t\t\tdisplay: flex;\n\t\t\t\talign-items: center;\n\t\t\t\tmax-width: 32rem;\n\t\t\t\tmargin: 0 1rem;\n\t\t\t}\n\n\t\t\t.status {\n\t\t\t\tfont-weight: 200;\n\t\t\t\tfont-size: 3rem;\n\t\t\t\tline-height: 1;\n\t\t\t\tposition: relative;\n\t\t\t\ttop: -0.05rem;\n\t\t\t}\n\n\t\t\t.message {\n\t\t\t\tborder-left: 1px solid var(--divider);\n\t\t\t\tpadding: 0 0 0 1rem;\n\t\t\t\tmargin: 0 0 0 1rem;\n\t\t\t\tmin-height: 2.5rem;\n\t\t\t\tdisplay: flex;\n\t\t\t\talign-items: center;\n\t\t\t}\n\n\t\t\t.message h1 {\n\t\t\t\tfont-weight: 400;\n\t\t\t\tfont-size: 1em;\n\t\t\t\tmargin: 0;\n\t\t\t}\n\n\t\t\t@media (prefers-color-scheme: dark) {\n\t\t\t\tbody {\n\t\t\t\t\t--bg: #222;\n\t\t\t\t\t--fg: #ddd;\n\t\t\t\t\t--divider: #666;\n\t\t\t\t}\n\t\t\t}\n\t\t</style>\n\t</head>\n\t<body>\n\t\t<div class=\"error\">\n\t\t\t<span class=\"status\">" + status + "</span>\n\t\t\t<div class=\"message\">\n\t\t\t\t<h1>" + message + "</h1>\n\t\t\t</div>\n\t\t</div>\n\t</body>\n</html>\n"
	},
	version_hash: "1gwcsxo"
};

export function get_hooks() {
	return {};
}

export { set_assets, set_building, set_private_env, set_public_env };
