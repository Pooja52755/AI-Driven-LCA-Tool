<script>
	export let results;
	export let circularityData;

	import { formatNumber, formatPercentage, getPerformanceLevel, getEmissionLevel } from '$lib/utils.js';

	$: emissionLevel = getEmissionLevel(results?.gwp || 0);
	$: circularityLevel = getPerformanceLevel(results?.circularity_score || 0);
</script>

<div class="max-w-6xl mx-auto">
	<div class="bg-white rounded-lg shadow-lg p-6">
		<!-- Header -->
		<div class="mb-8">
			<h2 class="text-2xl font-bold text-gray-900 mb-2">LCA Analysis Results</h2>
			<p class="text-gray-600">{results?.metal_type} ({results?.process_route} Route) - Environmental Impact Assessment</p>
		</div>

		<!-- Key Metrics -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
			<!-- GWP -->
			<div class="metric-card bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-lg border border-red-200">
				<div class="flex items-center justify-between">
					<div>
						<h3 class="text-lg font-semibold text-red-900">GWP</h3>
						<p class="text-3xl font-bold text-red-700">{formatNumber(results?.gwp || 0, 1)}</p>
						<p class="text-sm text-red-600 mt-1">kg CO₂e/tonne</p>
					</div>
					<div class="text-4xl text-red-400">🌡️</div>
				</div>
				<div class="mt-4">
					<span class="px-2 py-1 text-xs rounded-full {emissionLevel.bg} {emissionLevel.color}">{emissionLevel.level}</span>
				</div>
			</div>

			<!-- Circularity Score -->
			<div class="metric-card bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
				<div class="flex items-center justify-between">
					<div>
						<h3 class="text-lg font-semibold text-green-900">Circularity</h3>
						<p class="text-3xl font-bold text-green-700">{formatPercentage(results?.circularity_score || 0, 0)}</p>
						<p class="text-sm text-green-600 mt-1">Score</p>
					</div>
					<div class="text-4xl text-green-400">♻️</div>
				</div>
				<div class="mt-4">
					<span class="px-2 py-1 text-xs rounded-full {circularityLevel.bg} {circularityLevel.color}">{circularityLevel.level}</span>
				</div>
			</div>

			<!-- Acidification -->
			<div class="metric-card bg-gradient-to-br from-yellow-50 to-yellow-100 p-6 rounded-lg border border-yellow-200">
				<div class="flex items-center justify-between">
					<div>
						<h3 class="text-lg font-semibold text-yellow-900">Acidification</h3>
						<p class="text-3xl font-bold text-yellow-700">{formatNumber(results?.acidification_potential || 0, 3)}</p>
						<p class="text-sm text-yellow-600 mt-1">kg SO₂ eq/tonne</p>
					</div>
					<div class="text-4xl text-yellow-400">💨</div>
				</div>
			</div>

			<!-- Eutrophication -->
			<div class="metric-card bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200">
				<div class="flex items-center justify-between">
					<div>
						<h3 class="text-lg font-semibold text-blue-900">Eutrophication</h3>
						<p class="text-3xl font-bold text-blue-700">{formatNumber(results?.eutrophication_potential || 0, 3)}</p>
						<p class="text-sm text-blue-600 mt-1">kg PO₄³⁻ eq/tonne</p>
					</div>
					<div class="text-4xl text-blue-400">💧</div>
				</div>
			</div>
		</div>

		<!-- Summary -->
		<div class="bg-gradient-to-r from-teal-50 to-blue-50 border border-teal-200 rounded-lg p-6">
			<h3 class="text-lg font-semibold text-gray-900 mb-4">Analysis Summary</h3>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div>
					<h4 class="font-medium text-gray-800 mb-2">Environmental Performance</h4>
					<p class="text-sm text-gray-600">
						The {results?.metal_type} {results?.process_route.toLowerCase()} production shows 
						{emissionLevel.level.toLowerCase()} carbon emissions at {formatNumber(results?.gwp || 0, 1)} kg CO₂e/tonne.
					</p>
				</div>
				<div>
					<h4 class="font-medium text-gray-800 mb-2">Circularity Performance</h4>
					<p class="text-sm text-gray-600">
						Circularity score of {formatPercentage(results?.circularity_score || 0, 0)} indicates 
						{circularityLevel.level.toLowerCase()} material flow efficiency and recycling potential.
					</p>
				</div>
			</div>
		</div>
	</div>
</div>