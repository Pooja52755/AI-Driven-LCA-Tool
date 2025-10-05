<script>
	import { onMount } from 'svelte';
	import { apiService } from '$lib/api.js';
	import ProcessInput from '$lib/components/ProcessInput.svelte';
	import ResultsDashboard from '$lib/components/ResultsDashboard.svelte';
	import CircularityGraph from '$lib/components/CircularityGraph.svelte';
	import ModelMetrics from '$lib/components/ModelMetrics.svelte';
	import ComparisonView from '$lib/components/ComparisonView.svelte';
	import { createToast } from '$lib/utils.js';

	// State variables
	let activeTab = 'input';
	let isLoading = false;
	let apiHealth = { status: 'unknown', components: {} };
	let currentResults = null;
	let currentCircularity = null;
	let processGraphData = null;
	let modelMetrics = null;
	let comparisons = [];

	// Tab management
	const tabs = [
		{ id: 'input', label: 'Process Input', icon: '⚙️' },
		{ id: 'results', label: 'LCA Results', icon: '📊' },
		{ id: 'circularity', label: 'Circularity Analysis', icon: '♻️' },
		{ id: 'comparison', label: 'Process Comparison', icon: '⚖️' },
		{ id: 'metrics', label: 'Model Validation', icon: '🎯' }
	];

	onMount(async () => {
		await checkApiHealth();
		await loadModelMetrics();
	});

	async function checkApiHealth() {
		try {
			apiHealth = await apiService.checkHealth();
			if (apiHealth.status === 'healthy') {
				createToast('API connection established successfully', 'success');
			}
		} catch (error) {
			console.error('API health check failed:', error);
			createToast('API connection failed. Please check backend status.', 'error');
		}
	}

	async function loadModelMetrics() {
		try {
			modelMetrics = await apiService.getModelMetrics();
		} catch (error) {
			console.error('Failed to load model metrics:', error);
		}
	}

	async function handleProcessAnalysis(event) {
		const processData = event.detail;
		isLoading = true;

		try {
			// Perform LCA analysis
			currentResults = await apiService.analyzeLCA(processData);
			
			// Perform circularity analysis
			currentCircularity = await apiService.analyzeCircularity(processData);
			
			// Switch to results tab
			activeTab = 'results';
			
			createToast('Analysis completed successfully!', 'success');
		} catch (error) {
			console.error('Analysis failed:', error);
			createToast(`Analysis failed: ${error.message}`, 'error');
		} finally {
			isLoading = false;
		}
	}

	async function handleComparisonRequest(event) {
		const processes = event.detail;
		isLoading = true;

		try {
			const result = await apiService.compareProcesses(processes);
			// Backend returns 'scenarios' not 'comparisons'
			comparisons = result.scenarios || result.comparisons || [];
			activeTab = 'comparison';
			createToast('Process comparison completed!', 'success');
		} catch (error) {
			console.error('Comparison failed:', error);
			createToast(`Comparison failed: ${error.message}`, 'error');
		} finally {
			isLoading = false;
		}
	}

	async function setActiveTab(tabId) {
		activeTab = tabId;
		
		// Load stored comparisons when switching to comparison tab
		if (tabId === 'comparison') {
			await loadStoredComparisons();
		}
	}

	async function loadStoredComparisons() {
		try {
			// Add getStoredComparisons method to apiService if it doesn't exist
			const result = await apiService.getStoredComparisons();
			
			// Transform stored analyses into comparison format
			if (result.analyses && result.analyses.length >= 2) {
				comparisons = result.analyses.map(analysis => ({
					process: analysis.input,
					lca: analysis.results
				}));
			} else {
				comparisons = [];
			}
		} catch (error) {
			console.error('Failed to load stored comparisons:', error);
			comparisons = [];
		}
	}
</script>

<svelte:head>
	<title>AI-Driven LCA Tool for Metallurgy - SIH 2025</title>
	<meta name="description" content="Advanced Life Cycle Assessment platform for metals and mining with AI-powered circularity analysis" />
</svelte:head>

<!-- Header -->
<header class="gradient-bg text-white shadow-lg">
	<div class="container mx-auto px-4 py-6">
		<div class="flex items-center justify-between">
			<div class="flex items-center space-x-4">
				<div class="w-12 h-12 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
					<span class="text-2xl">🏭</span>
				</div>
				<div>
					<h1 class="text-2xl font-bold">AI-Driven LCA Tool</h1>
					<p class="text-teal-100">Metallurgy & Mining Sustainability Platform</p>
				</div>
			</div>
			
			<div class="flex items-center space-x-4">
				<div class="text-right">
					<p class="text-sm text-teal-100">SIH 2025 - Problem Statement 25069</p>
					<div class="flex items-center space-x-2">
						<span class="w-2 h-2 rounded-full {apiHealth.status === 'healthy' ? 'bg-green-400' : 'bg-red-400'}"></span>
						<span class="text-sm">{apiHealth.status === 'healthy' ? 'Connected' : 'Disconnected'}</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</header>

<!-- Navigation Tabs -->
<nav class="bg-white shadow-sm border-b">
	<div class="container mx-auto px-4">
		<div class="flex space-x-1 overflow-x-auto">
			{#each tabs as tab}
				<button
					class="flex items-center space-x-2 px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors duration-200 border-b-2 {
						activeTab === tab.id 
							? 'border-teal-600 text-teal-600 bg-teal-50' 
							: 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
					}"
					on:click={() => setActiveTab(tab.id)}
				>
					<span class="text-lg">{tab.icon}</span>
					<span>{tab.label}</span>
				</button>
			{/each}
		</div>
	</div>
</nav>

<!-- Main Content -->
<main class="container mx-auto px-4 py-8 min-h-screen">
	{#if isLoading}
		<div class="flex items-center justify-center py-12">
			<div class="text-center">
				<div class="loading-spinner mx-auto mb-4"></div>
				<p class="text-gray-600">Processing analysis...</p>
			</div>
		</div>
	{:else}
		<!-- Process Input Tab -->
		{#if activeTab === 'input'}
			<div class="fade-in">
				<ProcessInput 
					on:analyzeProcess={handleProcessAnalysis}
					on:compareProcesses={handleComparisonRequest}
				/>
			</div>
		{/if}

		<!-- Results Dashboard Tab -->
		{#if activeTab === 'results'}
			<div class="fade-in">
				{#if currentResults}
					<ResultsDashboard 
						results={currentResults} 
						circularityData={currentCircularity}
					/>
				{:else}
					<div class="text-center py-12">
						<div class="w-16 h-16 bg-gray-100 rounded-full mx-auto mb-4 flex items-center justify-center">
							<span class="text-2xl text-gray-400">📊</span>
						</div>
						<h3 class="text-lg font-medium text-gray-900 mb-2">No Analysis Results</h3>
						<p class="text-gray-500 mb-4">Please run an analysis from the Process Input tab to see results here.</p>
						<button 
							class="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors"
							on:click={() => setActiveTab('input')}
						>
							Go to Process Input
						</button>
					</div>
				{/if}
			</div>
		{/if}

		<!-- Circularity Analysis Tab -->
		{#if activeTab === 'circularity'}
			<div class="fade-in">
				{#if currentCircularity}
					<CircularityGraph data={currentCircularity} />
				{:else}
					<div class="text-center py-12">
						<div class="w-16 h-16 bg-gray-100 rounded-full mx-auto mb-4 flex items-center justify-center">
							<span class="text-2xl text-gray-400">♻️</span>
						</div>
						<h3 class="text-lg font-medium text-gray-900 mb-2">No Circularity Analysis</h3>
						<p class="text-gray-500 mb-4">Please run an analysis to see circularity flow visualization.</p>
						<button 
							class="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors"
							on:click={() => setActiveTab('input')}
						>
							Start Analysis
						</button>
					</div>
				{/if}
			</div>
		{/if}

		<!-- Process Comparison Tab -->
		{#if activeTab === 'comparison'}
			<div class="fade-in">
				<ComparisonView data={comparisons} />
			</div>
		{/if}

		<!-- Model Metrics Tab -->
		{#if activeTab === 'metrics'}
			<div class="fade-in">
				{#if modelMetrics}
					<ModelMetrics data={modelMetrics} />
				{:else}
					<div class="text-center py-12">
						<div class="loading-spinner mx-auto mb-4"></div>
						<p class="text-gray-600">Loading model validation metrics...</p>
					</div>
				{/if}
			</div>
		{/if}
	{/if}
</main>

<!-- Footer -->
<footer class="bg-gray-50 border-t mt-auto">
	<div class="container mx-auto px-4 py-6">
		<div class="flex items-center justify-between text-sm text-gray-600">
			<div>
				<p>© 2025 AI-Driven LCA Tool for Metallurgy - SIH 2025</p>
				<p>Built with Svelte, FastAPI, Neo4j, and LightGBM</p>
			</div>
			<div class="text-right">
				<p>Problem Statement: 25069</p>
				<p>Advancing Circularity and Sustainability in Metallurgy and Mining</p>
			</div>
		</div>
	</div>
</footer>

<style>
	:global(.container) {
		max-width: 1200px;
	}
</style>