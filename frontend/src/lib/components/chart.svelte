<script lang="ts">
	import { browser } from '$app/environment';
	import Chart, { type ChartTypeRegistry } from 'chart.js/auto';
	import { onMount } from 'svelte';

	export let type: keyof ChartTypeRegistry;
	export let labels: string[];
	export let data: { label: string; values: number[] }[];

	let canvas: HTMLCanvasElement;
	let chart: Chart;
	const id = crypto.randomUUID();

	onMount(() => {
		if (browser) {
			console.log(
				JSON.stringify({
					data,
					labels
				})
			);

			chart = new Chart(canvas, {
				type,
				data: {
					labels: labels,
					datasets: data.map((d) => ({
						label: d.label,
						data: d.values,
						borderWidth: type === 'pie' ? 0 : undefined,
						showLine: true
						// fill: true,
					}))
				},
				options: {},
				plugins: [
					{
						id: 'plugin',
						// https://stackoverflow.com/a/59653241
						afterDraw(chart) {
							// eslint-disable-next-line @typescript-eslint/no-unsafe-call
							if (
								chart.data.datasets.every((dataset) => dataset.data.every((item) => item === 0))
							) {
								const { ctx, width, height } = chart;

								chart.clear();
								ctx.save();
								ctx.textAlign = 'center';
								ctx.textBaseline = 'middle';
								ctx.font = "16px normal 'Helvetica Nueue'";
								ctx.fillText('No data to display', width / 2, height / 3);
								ctx.restore();
							}
						}
					}
				]
			});
		}
	});
</script>

<canvas
	{id}
	bind:this={canvas}
	class="mr-2 {type === 'line' ? 'w-[70vw] h-[35vh]' : 'w-[35vw] h-[35vh]'}"
>
</canvas>
