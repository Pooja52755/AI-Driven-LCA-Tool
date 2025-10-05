<script>
	export let data;

	import { onMount } from 'svelte';
	import { formatPercentage } from '$lib/utils.js';

	let networkContainer;

	onMount(() => {
		if (typeof vis !== 'undefined') {
			createCircularityNetwork();
		}
	});

	function createCircularityNetwork() {
		// Mock circularity graph data
		const nodes = new vis.DataSet([
			{id: 1, label: 'Raw Materials\n(Virgin/Scrap)', group: 'input', x: -200, y: 0},
			{id: 2, label: 'Processing\n(Smelting)', group: 'process', x: 0, y: 0},
			{id: 3, label: 'Product\n(Metal)', group: 'output', x: 200, y: 0},
			{id: 4, label: 'Use Phase', group: 'use', x: 200, y: 100},
			{id: 5, label: 'End of Life', group: 'eol', x: 0, y: 100},
			{id: 6, label: 'Recycling', group: 'recycling', x: -200, y: 100},
			{id: 7, label: 'Waste', group: 'waste', x: 0, y: 200}
		]);

		const edges = new vis.DataSet([
			{from: 1, to: 2, label: '100%', arrows: 'to', color: '#0f766e', width: 3},
			{from: 2, to: 3, label: '85%', arrows: 'to', color: '#0f766e', width: 3},
			{from: 3, to: 4, label: '100%', arrows: 'to', color: '#0f766e', width: 2},
			{from: 4, to: 5, label: '100%', arrows: 'to', color: '#0f766e', width: 2},
			{from: 5, to: 6, label: '70%', arrows: 'to', color: '#10b981', width: 4},
			{from: 5, to: 7, label: '30%', arrows: 'to', color: '#ef4444', width: 2},
			{from: 6, to: 1, label: 'Recycled Content', arrows: 'to', color: '#10b981', width: 4, dashes: true},
			{from: 2, to: 7, label: '15%', arrows: 'to', color: '#ef4444', width: 1}
		]);

		const options = {
			groups: {
				input: {color: {background: '#dbeafe', border: '#3b82f6'}, shape: 'box'},
				process: {color: {background: '#fef3c7', border: '#f59e0b'}, shape: 'ellipse'},
				output: {color: {background: '#d1fae5', border: '#10b981'}, shape: 'box'},
				use: {color: {background: '#e0e7ff', border: '#6366f1'}, shape: 'box'},
				eol: {color: {background: '#fce7f3', border: '#ec4899'}, shape: 'diamond'},
				recycling: {color: {background: '#d1fae5', border: '#10b981'}, shape: 'triangle'},
				waste: {color: {background: '#fee2e2', border: '#ef4444'}, shape: 'box'}
			},
			layout: {
				hierarchical: false
			},
			physics: {
				enabled: false
			},
			nodes: {
				font: {size: 12, color: '#374151'},
				borderWidth: 2,
				shadow: true
			},
			edges: {
				font: {size: 10, color: '#6b7280'},
				shadow: true,
				smooth: {type: 'cubicBezier', forceDirection: 'horizontal'}
			}
		};

		const network = new vis.Network(networkContainer, {nodes, edges}, options);
	}
</script>

<div class="max-w-6xl mx-auto">
	<div class="bg-white rounded-lg shadow-lg p-6">
		<!-- Header -->
		<div class="mb-6">
			<h2 class="text-2xl font-bold text-gray-900 mb-2">Circularity Flow Analysis</h2>
			<p class="text-gray-600">Interactive material flow visualization showing circular economy opportunities</p>
		</div>

		<!-- Circularity Metrics -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
			<div class="bg-green-50 border border-green-200 rounded-lg p-4">
				<h3 class="font-semibold text-green-900">Current Circularity</h3>
				<p class="text-2xl font-bold text-green-700">{formatPercentage(data?.current_score || 65, 0)}</p>
				<p class="text-sm text-green-600">Material loops active</p>
			</div>
			<div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
				<h3 class="font-semibold text-blue-900">Optimal Potential</h3>
				<p class="text-2xl font-bold text-blue-700">{formatPercentage(data?.optimal_score || 87, 0)}</p>
				<p class="text-sm text-blue-600">Maximum achievable</p>
			</div>
			<div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
				<h3 class="font-semibold text-purple-900">Improvement Gap</h3>
				<p class="text-2xl font-bold text-purple-700">{formatPercentage((data?.optimal_score || 87) - (data?.current_score || 65), 0)}</p>
				<p class="text-sm text-purple-600">Optimization opportunity</p>
			</div>
		</div>

		<!-- Network Visualization -->
		<div class="mb-6">
			<h3 class="text-lg font-semibold text-gray-900 mb-4">Material Flow Network</h3>
			<div bind:this={networkContainer} class="vis-network"></div>
		</div>

		<!-- Legend -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<div>
				<h4 class="font-medium text-gray-800 mb-3">Flow Legend</h4>
				<div class="space-y-2 text-sm">
					<div class="flex items-center space-x-2">
						<div class="w-4 h-1 bg-green-500"></div>
						<span>Circular flows (recycling loops)</span>
					</div>
					<div class="flex items-center space-x-2">
						<div class="w-4 h-1 bg-teal-600"></div>
						<span>Primary production flows</span>
					</div>
					<div class="flex items-center space-x-2">
						<div class="w-4 h-1 bg-red-500"></div>
						<span>Waste streams (linear flows)</span>
					</div>
				</div>
			</div>
			<div>
				<h4 class="font-medium text-gray-800 mb-3">Optimization Opportunities</h4>
				<ul class="space-y-1 text-sm text-gray-600">
					<li>• Increase recycled content to 80%+</li>
					<li>• Reduce waste streams by 15%</li>
					<li>• Implement closed-loop water systems</li>
					<li>• Optimize energy recovery processes</li>
				</ul>
			</div>
		</div>
	</div>
</div>