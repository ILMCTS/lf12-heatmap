<script lang="ts">
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
	let startMondayOffset: number | null = null;
	let weeks: (number | null)[][] = [];

	if (data.length > 0) {
		firstDate = new Date(data[0].startDate);
		lastDate = new Date(data[data.length - 1].endDate);
		year = firstDate.getFullYear();
		monthIdx = firstDate.getMonth();
		monthDayCount = new Date(year, monthIdx + 1, 0).getDate();
		startMondayOffset = 1;

		const fullWeeks = monthDayCount + startMondayOffset;

		for (let i = 0; i < fullWeeks + Math.ceil(fullWeeks / 7); i += 1) {
			const week = Math.trunc(i / daysPerWeek);

			weeks[week] ??= [];
			weeks[week].push(
				i < startMondayOffset || monthDayCount < i ? null : i - startMondayOffset + 1
			);
		}
	}
</script>

{#if firstDate && lastDate && monthIdx && monthDayCount && year}
	{JSON.stringify(weeks)}

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

		{#each weeks as week}
			<div class="grid grid-flow-col">
				{#each week as day}
					<div class="w-8 h-8">
						{#if day}
							{day}
						{/if}
					</div>
				{/each}
			</div>
		{/each}
	</div>
{/if}
