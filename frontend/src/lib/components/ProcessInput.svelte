<script>
	import { createEventDispatcher } from 'svelte';
	import { SUPPORTED_METALS, ENERGY_SOURCES, INDIAN_LOCATIONS, validateProcessInput } from '$lib/utils.js';

	const dispatch = createEventDispatcher();

	// Form data
	let processData = {
		metal_type: '',
		process_route: '',
		production_capacity: '',
		energy_source: '',
		energy_consumption: '',
		transport_distance: '',
		processing_location: '',
		ore_grade: '',
		end_of_life_option: '',
		recycling_rate: ''
	};

	// Validation
	let errors = {};
	let isSubmitting = false;

	// Multiple processes for comparison
	let comparisonProcesses = [];
	let showComparison = false;

	function handleSubmit() {
		const validation = validateProcessInput(processData);
		errors = validation.errors;

		if (validation.isValid) {
			isSubmitting = true;
			
			// Convert string numbers to numbers
			const processedData = {
				...processData,
				production_capacity: parseFloat(processData.production_capacity),
				energy_consumption: processData.energy_consumption ? parseFloat(processData.energy_consumption) : null,
				transport_distance: processData.transport_distance ? parseFloat(processData.transport_distance) : null,
				ore_grade: processData.ore_grade ? parseFloat(processData.ore_grade) : null,
				recycling_rate: processData.recycling_rate ? parseFloat(processData.recycling_rate) : null
			};

			dispatch('analyzeProcess', processedData);
			setTimeout(() => { isSubmitting = false; }, 2000);
		}
	}

	function addToComparison() {
		const validation = validateProcessInput(processData);
		if (validation.isValid) {
			const processedData = {
				...processData,
				name: `${processData.metal_type} - ${processData.process_route}`,
				production_capacity: parseFloat(processData.production_capacity),
				energy_consumption: processData.energy_consumption ? parseFloat(processData.energy_consumption) : null,
				transport_distance: processData.transport_distance ? parseFloat(processData.transport_distance) : null,
				ore_grade: processData.ore_grade ? parseFloat(processData.ore_grade) : null,
				recycling_rate: processData.recycling_rate ? parseFloat(processData.recycling_rate) : null
			};
			
			comparisonProcesses = [...comparisonProcesses, processedData];
			showComparison = true;
		} else {
			errors = validation.errors;
		}
	}

	function removeFromComparison(index) {
		comparisonProcesses = comparisonProcesses.filter((_, i) => i !== index);
		if (comparisonProcesses.length === 0) {
			showComparison = false;
		}
	}

	function runComparison() {
		if (comparisonProcesses.length >= 2) {
			dispatch('compareProcesses', comparisonProcesses);
		}
	}

	function clearForm() {
		processData = {
			metal_type: '',
			process_route: '',
			production_capacity: '',
			energy_source: '',
			energy_consumption: '',
			transport_distance: '',
			processing_location: '',
			ore_grade: '',
			end_of_life_option: '',
			recycling_rate: ''
		};
		errors = {};
	}

	function loadExampleData() {
		processData = {
			metal_type: 'Aluminium',
			process_route: 'Primary',
			production_capacity: '7500',
			energy_source: 'Mixed (Coal + Solar)',
			energy_consumption: '45',
			transport_distance: '125',
			processing_location: 'Odisha, India',
			ore_grade: '1.5',
			end_of_life_option: 'Recycling',
			recycling_rate: '65'
		};
		errors = {};
	}
</script>

<div class="max-w-4xl mx-auto">
	<div class="bg-white rounded-lg shadow-lg p-6">
		<!-- Header -->
		<div class="flex items-center justify-between mb-6">
			<div>
				<h2 class="text-2xl font-bold text-gray-900">Process Input & Configuration</h2>
				<p class="text-gray-600 mt-1">Configure metallurgy process parameters for LCA analysis</p>
			</div>
			<div class="flex space-x-2">
				<button
					type="button"
					class="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
					on:click={loadExampleData}
				>
					Load Example
				</button>
				<button
					type="button"
					class="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
					on:click={clearForm}
				>
					Clear Form
				</button>
			</div>
		</div>

		<form on:submit|preventDefault={handleSubmit} class="space-y-6">
			<!-- Basic Process Configuration -->
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<!-- Metal Type -->
				<div>
					<label for="metal_type" class="block text-sm font-medium text-gray-700 mb-2">
						Metal Type *
					</label>
					<select
						id="metal_type"
						bind:value={processData.metal_type}
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.metal_type ? 'border-red-500' : ''}"
						required
					>
						<option value="">Select metal type</option>
						{#each SUPPORTED_METALS as metal}
							<option value={metal.name}>{metal.name} ({metal.symbol})</option>
						{/each}
					</select>
					{#if errors.metal_type}
						<p class="text-red-500 text-sm mt-1">{errors.metal_type}</p>
					{/if}
				</div>

				<!-- Process Route -->
				<div>
					<label for="process_route" class="block text-sm font-medium text-gray-700 mb-2">
						Process Route *
					</label>
					<select
						id="process_route"
						bind:value={processData.process_route}
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.process_route ? 'border-red-500' : ''}"
						required
					>
						<option value="">Select process route</option>
						<option value="Primary">Primary (Virgin Material)</option>
						<option value="Recycled">Recycled (Secondary Material)</option>
					</select>
					{#if errors.process_route}
						<p class="text-red-500 text-sm mt-1">{errors.process_route}</p>
					{/if}
				</div>
			</div>

			<!-- Production Details -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
				<!-- Production Capacity -->
				<div>
					<label for="production_capacity" class="block text-sm font-medium text-gray-700 mb-2">
						Production Capacity (tonnes/year) *
					</label>
					<input
						type="number"
						id="production_capacity"
						bind:value={processData.production_capacity}
						placeholder="e.g., 5000"
						min="1"
						step="100"
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.production_capacity ? 'border-red-500' : ''}"
						required
					>
					{#if errors.production_capacity}
						<p class="text-red-500 text-sm mt-1">{errors.production_capacity}</p>
					{/if}
				</div>

				<!-- Energy Consumption -->
				<div>
					<label for="energy_consumption" class="block text-sm font-medium text-gray-700 mb-2">
						Energy Consumption (MW) <span class="text-gray-500">🤖 AI Predicted</span>
					</label>
					<input
						type="number"
						id="energy_consumption"
						bind:value={processData.energy_consumption}
						placeholder="AI will predict if empty"
						min="0"
						step="0.1"
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.energy_consumption ? 'border-red-500' : ''}"
					>
					{#if errors.energy_consumption}
						<p class="text-red-500 text-sm mt-1">{errors.energy_consumption}</p>
					{/if}
				</div>

				<!-- Transport Distance -->
				<div>
					<label for="transport_distance" class="block text-sm font-medium text-gray-700 mb-2">
						Transport Distance (km) <span class="text-gray-500">🤖 AI Predicted</span>
					</label>
					<input
						type="number"
						id="transport_distance"
						bind:value={processData.transport_distance}
						placeholder="AI will predict if empty"
						min="0"
						step="1"
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.transport_distance ? 'border-red-500' : ''}"
					>
					{#if errors.transport_distance}
						<p class="text-red-500 text-sm mt-1">{errors.transport_distance}</p>
					{/if}
				</div>
			</div>

			<!-- Location and Energy -->
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<!-- Processing Location -->
				<div>
					<label for="processing_location" class="block text-sm font-medium text-gray-700 mb-2">
						Processing Location *
					</label>
					<select
						id="processing_location"
						bind:value={processData.processing_location}
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.processing_location ? 'border-red-500' : ''}"
						required
					>
						<option value="">Select processing location</option>
						{#each INDIAN_LOCATIONS as location}
							<option value={location}>{location}</option>
						{/each}
					</select>
					{#if errors.processing_location}
						<p class="text-red-500 text-sm mt-1">{errors.processing_location}</p>
					{/if}
				</div>

				<!-- Energy Source -->
				<div>
					<label for="energy_source" class="block text-sm font-medium text-gray-700 mb-2">
						Energy Source *
					</label>
					<select
						id="energy_source"
						bind:value={processData.energy_source}
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.energy_source ? 'border-red-500' : ''}"
						required
					>
						<option value="">Select energy source</option>
						{#each ENERGY_SOURCES as source}
							<option value={source}>{source}</option>
						{/each}
					</select>
					{#if errors.energy_source}
						<p class="text-red-500 text-sm mt-1">{errors.energy_source}</p>
					{/if}
				</div>
			</div>

			<!-- Advanced Parameters -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
				<!-- Ore Grade -->
				<div>
					<label for="ore_grade" class="block text-sm font-medium text-gray-700 mb-2">
						Ore Grade (%) <span class="text-gray-500">🤖 AI Predicted</span>
					</label>
					<input
						type="number"
						id="ore_grade"
						bind:value={processData.ore_grade}
						placeholder="AI will predict if empty"
						min="0"
						max="100"
						step="0.1"
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.ore_grade ? 'border-red-500' : ''}"
					>
					{#if errors.ore_grade}
						<p class="text-red-500 text-sm mt-1">{errors.ore_grade}</p>
					{/if}
				</div>

				<!-- Recycling Rate -->
				<div>
					<label for="recycling_rate" class="block text-sm font-medium text-gray-700 mb-2">
						Recycling Rate (%) <span class="text-gray-500">🤖 AI Predicted</span>
					</label>
					<input
						type="number"
						id="recycling_rate"
						bind:value={processData.recycling_rate}
						placeholder="AI will predict if empty"
						min="0"
						max="100"
						step="0.1"
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.recycling_rate ? 'border-red-500' : ''}"
					>
					{#if errors.recycling_rate}
						<p class="text-red-500 text-sm mt-1">{errors.recycling_rate}</p>
					{/if}
				</div>

				<!-- End of Life Option -->
				<div>
					<label for="end_of_life_option" class="block text-sm font-medium text-gray-700 mb-2">
						End of Life Option *
					</label>
					<select
						id="end_of_life_option"
						bind:value={processData.end_of_life_option}
						class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 {errors.end_of_life_option ? 'border-red-500' : ''}"
						required
					>
						<option value="">Select end of life option</option>
						<option value="Recycling">Recycling</option>
						<option value="Landfill">Landfill</option>
						<option value="Recycling / Landfill">Mixed (Recycling + Landfill)</option>
					</select>
					{#if errors.end_of_life_option}
						<p class="text-red-500 text-sm mt-1">{errors.end_of_life_option}</p>
					{/if}
				</div>
			</div>

			<!-- Action Buttons -->
			<div class="flex flex-wrap gap-4 pt-6 border-t">
				<button
					type="submit"
					disabled={isSubmitting}
					class="flex items-center space-x-2 bg-teal-600 text-white px-6 py-3 rounded-lg hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
				>
					{#if isSubmitting}
						<div class="loading-spinner w-4 h-4"></div>
					{:else}
						<span>🔬</span>
					{/if}
					<span>Run LCA Analysis</span>
				</button>

				<button
					type="button"
					class="flex items-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
					on:click={addToComparison}
				>
					<span>➕</span>
					<span>Add to Comparison</span>
				</button>

				{#if showComparison && comparisonProcesses.length >= 2}
					<button
						type="button"
						class="flex items-center space-x-2 bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors"
						on:click={runComparison}
					>
						<span>⚖️</span>
						<span>Compare Processes ({comparisonProcesses.length})</span>
					</button>
				{/if}
			</div>
		</form>

		<!-- Comparison Queue -->
		{#if showComparison && comparisonProcesses.length > 0}
			<div class="mt-8 p-4 bg-gray-50 rounded-lg">
				<h3 class="text-lg font-medium text-gray-900 mb-4">Comparison Queue ({comparisonProcesses.length} processes)</h3>
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
					{#each comparisonProcesses as process, index}
						<div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
							<div class="flex items-start justify-between">
								<div class="flex-1 min-w-0">
									<p class="text-sm font-medium text-gray-900 truncate">{process.name}</p>
									<p class="text-xs text-gray-500">{process.processing_location}</p>
									<p class="text-xs text-gray-500">{process.production_capacity} tonnes/year</p>
								</div>
								<button
									class="ml-2 text-red-500 hover:text-red-700 text-sm"
									on:click={() => removeFromComparison(index)}
								>
									✕
								</button>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/if}
	</div>
</div>