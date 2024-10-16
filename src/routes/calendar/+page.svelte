<script lang="ts">
	const data = [
		{
			userId: 'scherwinsky_leander',
			firstName: 'Leander',
			lastName: 'Scherwinsky',
			startDate: '2024-10-08T06:00:00.000Z',
			endDate: '2024-10-10T15:30:00.000Z',
			status: 'A',
			customText: ''
		},
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
	const reasonColors: Record<string, string> = {
		A: 'bg-green-500', // Attest
		P: 'bg-red-200', // Privat
		S: 'bg-red-700' // Schulische Abwesenheit
	};

	let firstDate: Date | null = null;
	let lastDate: Date | null = null;
	let year: number | null = null;
	let monthIdx: number | null = null;
	let monthDayCount: number | null = null;
	let startMondayOffset: number | null = null;
	let weeks: { day: number; display: boolean }[][] = [];

	if (data.length > 0) {
		firstDate = new Date(data[0].startDate);
		lastDate = new Date(data[data.length - 1].endDate);
		year = firstDate.getFullYear();
		monthIdx = firstDate.getMonth();
		monthDayCount = new Date(year, monthIdx + 1, 0).getDate();
		startMondayOffset = 1;

		// October 2024: 31 + 1 -> 32
		const fullWeeks = monthDayCount + startMondayOffset;
		const fillDays = Math.ceil(fullWeeks / daysPerWeek); // ceil(32 / 7) -> 5

		// October 2024: 32 + 5 - (7 - 5) -> 35 (1 for start offset, 3 for final offset)
		for (let i = 0; i < fullWeeks + fillDays - (daysPerWeek - fillDays); i += 1) {
			const week = Math.trunc(i / daysPerWeek);
			const day = i - startMondayOffset + 1;

			weeks[week] ??= [];
			weeks[week].push({
				day,
				display: !(i < startMondayOffset || monthDayCount < i)
			});
		}
	}
</script>

{#if firstDate && lastDate && monthIdx && monthDayCount && year}
	<div class="text-xl">
		Monat: {new Intl.DateTimeFormat('de', { month: 'long' }).formatToParts(
			new Date(year, monthIdx)
		)[0].value}
	</div>

	<div class="grid grid-flow-row text-center">
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
			<div class="grid grid-cols-7 grid-flow-col">
				{#each week as { day, display }}
					{@const date = new Date(year, monthIdx, day)}
					{@const absence =
						display &&
						data.find((x) => {
							const startDate = new Date(x.startDate);
							const endDate = new Date(x.endDate);

							// too early
							if (date.getMonth() < startDate.getMonth()) {
								return false;
							}

							// too late
							if (endDate.getMonth() < date.getMonth()) {
								return false;
							}

							// first or last day of absence
							if (date.getDate() === startDate.getDate() || date.getDate() === endDate.getDate()) {
								return true;
							}

							// within time frame
							return startDate < date && date < endDate;
						})}

					<div class="p-2 {absence ? reasonColors[absence.status] || 'bg-blue-400' : ''}">
						{#if display}
							{day}
						{/if}
					</div>
				{/each}
			</div>
		{/each}
	</div>
{/if}
