<script>
	export let data;

	import { formatNumber, formatPercentage, getMetalColor } from '$lib/utils.js';

	$: comparisons = data || [];
</script>

<div class="max-w-6xl mx-auto">
	<div class="bg-white rounded-lg shadow-lg p-6">
		<!-- Header -->
		<div class="mb-8">
			<h2 class="text-2xl font-bold text-gray-900 mb-2">Process Comparison Analysis</h2>
			<p class="text-gray-600">Side-by-side comparison of different metallurgy processes</p>
		</div>

		{#if comparisons.length === 0}
			<div class="text-center py-12">
				<div class="w-16 h-16 bg-gray-100 rounded-full mx-auto mb-4 flex items-center justify-center">
					<span class="text-2xl text-gray-400">⚖️</span>
				</div>
				<h3 class="text-lg font-medium text-gray-900 mb-2">No Comparisons Available</h3>
				<p class="text-gray-500">Add multiple processes from the Input tab to compare their environmental impacts.</p>
			</div>
		{:else}
			<!-- Comparison Table -->
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y divide-gray-200">
					<thead class="bg-gray-50">
						<tr>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Process</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">GWP</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Circularity</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acidification</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Eutrophication</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Overall</th>
						</tr>
					</thead>
					<tbody class="bg-white divide-y divide-gray-200">
						{#each comparisons as comparison, index}
							<tr class="hover:bg-gray-50">
								<td class="px-6 py-4 whitespace-nowrap">
									<div class="flex items-center">
										<div class="w-3 h-3 rounded-full mr-3" style="background-color: {getMetalColor(comparison.process?.metal_type)}"></div>
										<div>
											<div class="text-sm font-medium text-gray-900">{comparison.process?.metal_type}</div>
											<div class="text-sm text-gray-500">{comparison.process?.process_route}</div>
										</div>
									</div>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
									{formatNumber(comparison.lca?.gwp || 0, 1)} kg CO₂e/t
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
									{formatPercentage(comparison.lca?.circularity_score || 0, 0)}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
									{formatNumber(comparison.lca?.acidification_potential || 0, 3)}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
									{formatNumber(comparison.lca?.eutrophication_potential || 0, 3)}
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">Good</span>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<!-- Summary -->
			<div class="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
				<h3 class="text-lg font-semibold text-blue-900 mb-4">Comparison Summary</h3>
				<p class="text-blue-800">Analyzed {comparisons.length} different processes. Recycled routes generally show 40-60% lower emissions than primary production.</p>
			</div>
		{/if}
	</div>
</div>