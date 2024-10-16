<script lang="ts">
	import { browser } from '$app/environment';

	const data = [
		{
			userId: 'scherwinsky_leander',
			firstName: 'Leander',
			lastName: 'Scherwinsky',
			startDate: '2024-10-17T06:00:00.000Z',
			endDate: '2024-10-17T07:30:00.000Z',
			status: 'S',
			customText: 'Kein Unterricht - Tr'
		}
	];

	const daysPerWeek = 7;

	let firstDate: Date | null = null;
	let lastDate: Date | null = null;
	let year: number | null = null;
	let monthIdx: number | null = null;
	let monthDayCount: number | null = null;

	if (data.length > 0) {
		firstDate = new Date(data[0].startDate);
		lastDate = new Date(data[data.length - 1].endDate);
		year = firstDate.getFullYear();
		monthIdx = firstDate.getMonth();
		monthDayCount = new Date(year, monthIdx + 1, 0).getDate();
	}
</script>

{#if firstDate && lastDate && monthIdx && monthDayCount && year}
	<!-- new Date(year, monthIdx + 1, 0).getDate() -->
	{@const startMondayOffset = 1}
	{@const days = new Array(monthDayCount + startMondayOffset).fill(null).reduce((prev, _, i) => {
		const week = Math.trunc(monthDayCount / 7);

		prev[week] ??= [];

		if (startMondayOffset < i) {
			prev[week].push(null);
		} else {
			const dayInMonth = week * daysPerWeek + (i / 7 + 1);

			prev[week].push(dayInMonth);
		}
	}, [])}
	{@const weekCount = Math.ceil(monthDayCount / 7)}

	{JSON.stringify(days)}

	<div>Monat: {monthIdx + 1}</div>

	<div class="grid grid-flow-row">
		<div class="grid grid-flow-col">
			<div>Montag</div>
			<div>Dienstag</div>
			<div>Mittwoch</div>
			<div>Donnerstag</div>
			<div>Freitag</div>
			<div>Samstag</div>
			<div>Sonntag</div>
		</div>

		{#each new Array(weekCount).fill(null) as _, i}
			<div class="grid grid-flow-col">
				{#each new Array(daysPerWeek).fill(null) as _, j}
					{@const dayInMonth = i * daysPerWeek + (j + 1)}

					<div class="w-8 h-8">
						{#if i === 0 && j < startMondayOffset}
							{dayInMonth}
						{:else if dayInMonth <= monthDayCount}
							{dayInMonth}
						{/if}
					</div>
				{/each}
			</div>
		{/each}
	</div>
{/if}
